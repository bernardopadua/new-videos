#include "deps/httplib.h"
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <ostream>
#include <string>
#include <chrono>

#include <filesystem>

std::string generateHashFileName(std::string ext){
    auto timestamp = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    uint32_t hash = static_cast<uint32_t>(std::hash<std::string>{}(std::to_string(timestamp)));

    std::stringstream strHash;
    strHash << std::hex << std::setfill('0') << std::setw(11) << hash;

    return strHash.str()+ext;
}

int main(int regv, char** regc){
    httplib::Server srv;

    srv.Post("/upload/avatar/temp", [](const httplib::Request &req, httplib::Response &res, const httplib::ContentReader &reader){
        std::ofstream fileUpload;
        std::string nameTempFile;

        reader([&fileUpload, &nameTempFile](const httplib::FormData &fileForm){
            int posDot = fileForm.filename.find_last_of(".");
            do {
                std::string ext = fileForm.filename.substr(posDot);
                nameTempFile = "/tmp/"+generateHashFileName(ext);
                std::cout << "FILENAME:" << nameTempFile << std::endl;
            } while (std::filesystem::exists(nameTempFile));

            fileUpload.open(nameTempFile, std::ios::binary);

            /*std::cout << fileForm.filename << std::endl;
            std::cout << fileForm.content << std::endl;
            std::cout << fileForm.content_type << std::endl;*/

            return true;
        }, [&fileUpload](const char* data, size_t size){
            fileUpload.write(data, size);
            return true;
        });
        fileUpload.close();

        std::string jsonReturn = "{\"filename\":\""+nameTempFile+"\"}";
        res.set_content(jsonReturn, "application/json");
    });

    srv.Get("/video/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string videoId = req.matches[1];
        std::string fileLoad = req.matches[2];

        std::string fileFolderLoad = "/usr/videos_data/"+videoId+"/"+fileLoad;
        std::ifstream fileLoadOpen(fileFolderLoad, std::ios::ate | std::ios::binary);
        
        if (!fileLoadOpen.is_open()){
            res.status = 404;
            res.set_content("<h1>This video does not exist.</h1>", "text/html");
            return;
        }

        std::streamsize sizeFile = fileLoadOpen.tellg();
        std::vector<char> fileBuffer(sizeFile);
        
        fileLoadOpen.seekg(0, std::ios::beg);
        fileLoadOpen.read(fileBuffer.data(), sizeFile);

        res.set_header("Access-Control-Allow-Origin", "http://localhost:8080");
        
        if (fileFolderLoad.substr(fileFolderLoad.length()-2) == "ts"){
            std::cout << "sending-MP2T: << " << fileFolderLoad << std::endl;
            res.set_content(fileBuffer.data(), sizeFile, "video/MP2T");    
        }

        std::cout << "sending-mpegURL: << " << fileFolderLoad << std::endl;
        res.set_content(fileBuffer.data(), sizeFile, "application/x-mpegURL");
    });

    std::cout << "Running..." << std::endl;
    srv.listen("0.0.0.0", 8099);
    return 0;
}