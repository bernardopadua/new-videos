#include "deps/httplib.h"
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <ostream>
#include <string>
#include <chrono>

#include <filesystem>

std::filesystem::path MEDIA_SERVER_BASE_PATH = "/usr/media_server/";
std::filesystem::path MEDIA_SERVER_TEMP_PATH = "/tmp/";

#define DOMAIN_WEB_SERVER "http://localhost:8080"

std::string generateHashFileName(std::string ext){
    auto timestamp = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    uint32_t hash = static_cast<uint32_t>(std::hash<std::string>{}(std::to_string(timestamp)));

    std::stringstream strHash;
    strHash << std::hex << std::setfill('0') << std::setw(11) << hash;

    return strHash.str()+ext;
}

int main(int regv, char** regc){
    httplib::Server srv;

    srv.Post("/upload/move/avatar/user/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        const std::string fileName = req.matches[2];
        const std::string userId = req.matches[1];
        
        if (!std::filesystem::exists(MEDIA_SERVER_TEMP_PATH / fileName)) {
            res.status = 404;
            res.set_content("{\"error\":\"File not found.\"}", "application/json");
            return;
        }

        //If file exists, move
        if (!std::filesystem::exists(MEDIA_SERVER_BASE_PATH.string()+"avatars/"+userId+"/")) {
            std::filesystem::create_directories(MEDIA_SERVER_BASE_PATH.string()+"avatars/"+userId+"/");
        }   
        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+fileName, 
            MEDIA_SERVER_BASE_PATH.string()+"avatars/"+userId+"/"+fileName
        );

        res.set_content("{\"success\":\"File moved successfully.\"}", "application/json");
    });

    srv.Post("/upload/avatar/temp", [](const httplib::Request &req, httplib::Response &res, const httplib::ContentReader &reader){
        std::ofstream fileUpload;
        std::string fileName;
        std::string nameTempFile;

        reader([&fileUpload, &nameTempFile, &fileName](const httplib::FormData &fileForm){
            int posDot = fileForm.filename.find_last_of(".");
            do {
                std::string ext = fileForm.filename.substr(posDot);
                fileName = generateHashFileName(ext);
                nameTempFile = "/tmp/"+fileName;
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

        std::string jsonReturn = "{\"filename\":\""+fileName+"\"}";
        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content(jsonReturn, "application/json");
    });

    srv.Get("/video/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string videoId = req.matches[1];
        std::string fileLoad = req.matches[2];

        std::string fileFolderLoad = MEDIA_SERVER_BASE_PATH.string()+"videos/"+videoId+"/"+fileLoad;
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
        
        if (fileFolderLoad.substr(fileFolderLoad.length()-2) == "ts"){
            std::cout << "sending-MP2T: << " << fileFolderLoad << std::endl;
            res.set_content(fileBuffer.data(), sizeFile, "video/MP2T");    
        }

        std::cout << "sending-mpegURL: << " << fileFolderLoad << std::endl;
        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content(fileBuffer.data(), sizeFile, "application/x-mpegURL");
    });

    std::cout << "Running..." << std::endl;
    srv.listen("0.0.0.0", 8099);
    return 0;
}