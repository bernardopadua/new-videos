#include "deps/httplib.h"
#include <string>

int main(int regv, char** regc){
    httplib::Server srv;

    srv.Post("/upload/avatar/temp", [](const httplib::Request &req, httplib::Response &res, const httplib::ContentReader &reader){
        auto formData = req.form.get_file(const std::string &fileName);
        /*std::ofstream fileUpload("/tmp/", std::ios::binary);
        reader([&fileUpload](const char* data, size_t size){
            fileUpload.write(data, size);
        });
        fileUpload.close();*/
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