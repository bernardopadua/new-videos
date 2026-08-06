#include "deps/httplib.h"
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <ostream>
#include <string>
#include <chrono>

#include <filesystem>

/*
    This "media-server" has no intent or purpose to be safe at the moment
    of this writting. So of course you can for example upload an ELF or something.
    This whole project is just a FUN and learning project.
*/

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
    const char* sss = std::getenv("DOMAIN_MEDIA_SERVER");

    if (sss == nullptr){
        std::cerr << "DOMAIN_MEDIA_SERVER is not set." << std::endl;
        return 1;
    }

    std::string thisDomain = std::string(sss);

    if(thisDomain.empty()){
        std::cerr << "DOMAIN_MEDIA_SERVER is not set." << std::endl;
        return 1;
    }

    /*
        CHANNEL IMAGES
    */
    //Generic GET for channel images, AVATAR and COVER/BANNER.
    srv.Get("/channel/([0-9]+)/image/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string channelId = req.matches[1];
        std::string typeImage = req.matches[2];
        std::string fileName = req.matches[3];
        std::string fileLoad = MEDIA_SERVER_BASE_PATH.string()+"channels/"+channelId+"/"+fileName;

        if (typeImage != "cover" && typeImage != "avatar"){
            res.status = 404;
            res.set_content("{\"error\":\"Type image is invalid.\"}", "application/json");
            return;
        }

        if (!std::filesystem::exists(fileLoad)){
            res.status = 404;
            res.set_content("<h1>File not found.</h1>", "text/html");
            return;
        }

        std::ifstream fileLoadOpen(fileLoad, std::ios::ate | std::ios::binary);

        if (!fileLoadOpen.is_open()){
            res.status = 404;
            res.set_content("<h1>This file could not be opened.</h1>", "text/html");
            return;
        }

        std::streamsize sizeFile = fileLoadOpen.tellg();
        std::vector<char> fileBuffer(sizeFile);

        fileLoadOpen.seekg(0, std::ios::beg);
        fileLoadOpen.read(fileBuffer.data(), sizeFile);

        int dotPos = fileName.find_last_of(".");
        std::string ext = fileName.substr(dotPos+1);

        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content(fileBuffer.data(), sizeFile, "image/"+ext);
    });
    
    //Move image from temp dir to finally directory. 
    //I maintain images in temp before move it to finally directory (after registration in DB).
    srv.Post("/channel/([^/]+)/move/image/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        const std::string fileName = req.matches[3];
        const std::string channelId = req.matches[1];
        const std::string typeImage = req.matches[2];

        if (typeImage != "cover" && typeImage != "avatar"){
            res.status = 404;
            res.set_content("{\"error\":\"Type image is invalid.\"}", "application/json");
            return;
        }
        
        if (!std::filesystem::exists(MEDIA_SERVER_TEMP_PATH / fileName)) {
            res.status = 404;
            res.set_content("{\"error\":\"File not found.\"}", "application/json");
            return;
        }

        //If file exists, move
        if (!std::filesystem::exists(MEDIA_SERVER_BASE_PATH.string()+"channels/"+channelId+"/")) {
            std::filesystem::create_directories(MEDIA_SERVER_BASE_PATH.string()+"channels/"+channelId+"/");
        }
        int dotPost = fileName.find_last_of('.');
        std::string ext = fileName.substr(dotPost);
        std::string newFilePath = MEDIA_SERVER_BASE_PATH.string()+"channel/" + channelId + "/" + typeImage + "_" + channelId + ext;
        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+fileName, 
            newFilePath
        );

        res.set_content("{ \
            \"success\":\"File moved successfully.\", \
            \"imageUrl\":\"/channels/" + channelId + "/image/" + typeImage + "/" + typeImage + "_" + channelId + ext + "\" \
            }", "application/json");
    });

    //Upload channel images to temp directory on media server.
    srv.Post("/channel/upload/image/temp", [](const httplib::Request &req, httplib::Response &res, const httplib::ContentReader &reader){
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

    /*
        END CHANNEL IMAGES
    */

    /*
        USER AVATAR
    */
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
        int dotPost = fileName.find_last_of('.');
        std::string ext = fileName.substr(dotPost);
        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+fileName, 
            MEDIA_SERVER_BASE_PATH.string()+"avatars/" + userId + "/user_" + userId + ext
        );

        res.set_content("{ \
            \"success\":\"File moved successfully.\", \
            \"userAvatarUrl\":\"/avatar/user/" + userId + "/" + "user_" + userId + ext + "\" \
            }", "application/json");
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

    srv.Get("/avatar/user/([0-9]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string userId = req.matches[1];
        std::string fileName = req.matches[2];

        std::string fileFolderLoad = MEDIA_SERVER_BASE_PATH.string()+"avatars/"+userId+"/"+fileName;
        std::ifstream fileLoadOpen(fileFolderLoad, std::ios::ate | std::ios::binary);

        int dotPos = fileName.find_last_of(".");
        std::string ext = fileName.substr(dotPos+1);

        if (!fileLoadOpen.is_open()){
            res.status = 404;
            res.set_content("<h1>This avatar does not exist.</h1>", "text/html");
            return;
        }

        std::streamsize sizeFile = fileLoadOpen.tellg();
        std::vector<char> fileBuffer(sizeFile);

        fileLoadOpen.seekg(0, std::ios::beg);
        fileLoadOpen.read(fileBuffer.data(), sizeFile);

        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content(fileBuffer.data(), sizeFile, "image/"+ext);
    });
    /*
        END USER AVATAR
    */

    /*
        VIDEO
    */
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
    /*
        END VIDEO
    */

    std::cout << "Running..." << std::endl;
    srv.listen("0.0.0.0", 8099);
    return 0;
}