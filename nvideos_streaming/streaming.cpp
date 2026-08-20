// Deps
#include "deps/httplib.h"
#include "deps/json.hpp"

// Libs
#include <cstddef>
#include <sw/redis++/redis++.h>

// System
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <ostream>
#include <string>
#include <chrono>
#include <filesystem>

/*
    This "media-server" has no intent or purpose to be safe at the moment
    of this writing. So of course you can for example upload an ELF or something.
    This whole project is just a FUN and learning project.
*/

std::filesystem::path MEDIA_SERVER_BASE_PATH = "/usr/media_server/";
std::filesystem::path MEDIA_SERVER_TEMP_PATH = "/tmp/";

std::string DOMAIN_WEB_SERVER = "http://localhost:8080";
std::string REDIS_ADDRESS = "tcp://localhost:6379";

std::string generateHashFileName(std::string ext){
    auto timestamp = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    uint32_t hash = static_cast<uint32_t>(std::hash<std::string>{}(std::to_string(timestamp)));

    std::stringstream strHash;
    strHash << std::hex << std::setfill('0') << std::setw(11) << hash;

    return strHash.str()+ext;
}

int main(int regv, char** regc){
    httplib::Server srv;
    sw::redis::Redis redis = sw::redis::Redis(REDIS_ADDRESS);
    std::string DOMAIN_MEDIA_SERVER(std::getenv("DOMAIN_MEDIA_SERVER"));

    if(DOMAIN_MEDIA_SERVER.empty()){
        std::cerr << "DOMAIN_MEDIA_SERVER is not set." << std::endl;
        return 1;
    }

    /*
        VIDEO
    */
    //Damn security stuff... praise security stuff. :)
    srv.Options("/video/init/upload", [](const httplib::Request &req, httplib::Response &res){
        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type");
        res.set_content("", "text/plain");
    });
    //Init video upload
    srv.Post("/video/init/upload", [&redis](const httplib::Request &req, httplib::Response &res){
        nlohmann::json payload;

        try {
            payload = nlohmann::json::parse(req.body);
        } catch(nlohmann::json::parse_error& e){
            res.status = 400;
            res.set_content("{\"error\": \"Failed to parse JSON body\"}", "application/json");
            return;
        }

        std::string fileName = payload["fileName"];
        int fileSize = payload["fileSize"];

        if (fileName.empty() || !fileSize || fileSize <= 0){
            res.status = 400;
            res.set_content("{\"error\": \"JSON is not valid\"}", "application/json");
            return;
        }

        nlohmann::json videoUpload = {
            {"name", fileName},
            {"totalSize", fileSize},
            {"uploadedSize", 0}
        };

        std::string UUID;
        do {
            UUID = generateHashFileName("");
        } while(redis.exists("video_upload:"+UUID));

        redis.set("video_upload:"+UUID, videoUpload.dump(), std::chrono::minutes(1));

        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content("{\"uuid\":\""+UUID+"\"}", "application/json");
    });
    //Upload video file
    srv.Post("/video/upload/([^/]+)", [&redis](const httplib::Request &req, httplib::Response &res, const httplib::ContentReader &reader){
        const std::string videoUUID = req.matches[1];
        std::string ext;
        std::ofstream fileUpload;


        //Avoiding CORS
        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);

        reader([&videoUUID, &res, &fileUpload, &ext](const httplib::FormData &fileForm){
            int dotPos = fileForm.filename.find_last_of(".");
            ext = fileForm.filename.substr(dotPos+1);
            
            if (std::filesystem::exists(MEDIA_SERVER_TEMP_PATH / (videoUUID + "." + ext))){
                res.status = 400;
                res.set_content("{\"error\":\"Video already exists\"}", "application/json");

                return false;
            }

            fileUpload.open(MEDIA_SERVER_TEMP_PATH / (videoUUID + "." + ext), std::ios::binary);
            if (!fileUpload.is_open()){
                res.status = 500;
                res.set_content("{\"error\":\"Failed to open file for writing\"}", "application/json");

                return false;
            }

            return true;
        },
        [&fileUpload, &redis, &videoUUID](const char *data, size_t size){
            fileUpload.write(data, size);
            auto fileUploaded = redis.get("video_upload:"+videoUUID);
            nlohmann::json j = nlohmann::json::parse(*fileUploaded);
            j["uploadedSize"] = j["uploadedSize"].get<int>() + size;

            redis.set("video_upload:"+videoUUID, j.dump(), std::chrono::minutes(1));

            return true;
        });

        fileUpload.close();
        res.set_content("{\"success\":true, \"filename\": \""+(videoUUID + "." + ext)+"\"}", "application/json");
    });
    //Upload video thumb to media server
    srv.Post("/video/upload/thumb/temp", [](const httplib::Request &req, httplib::Response &res, const httplib::ContentReader &reader){
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
    //Get upload status
    srv.Get("/video/upload/status/([^/]+)", [&redis](const httplib::Request &req, httplib::Response &res){
        const std::string videoUUID = req.matches[1];
        auto fileUploaded = redis.get("video_upload:"+videoUUID);
        
        if (!fileUploaded.has_value()) {
            res.status = 404;
            res.set_content("{\"error\":\"Video not found\"}", "application/json");
            return;
        }
        
        nlohmann::json j = nlohmann::json::parse(*fileUploaded);
        int uploadedSize = j["uploadedSize"] = j["uploadedSize"].get<int>();
        int totalSize = j["totalSize"].get<int>();
        int percent = (int)round((uploadedSize*100.0) / totalSize);

        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content("{\"percent\":"+std::to_string(percent)+"}", "application/json");
    });
    //Move thumbnail and video to video (video key) directory
    srv.Post("/video/move/file/temp/([^/]+)/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string videoKey = req.matches[1];
        std::string videoFileNameTemp = req.matches[2];
        std::string thumbnailFileNameTemp = req.matches[3];

        if (videoFileNameTemp.size() > 0 && !std::filesystem::exists(MEDIA_SERVER_TEMP_PATH / videoFileNameTemp)) {
            res.status = 404;
            res.set_content("{\"error\":\"Video file not found.\"}", "application/json");
            return;
        }
        if (thumbnailFileNameTemp.size() > 0 && !std::filesystem::exists(MEDIA_SERVER_TEMP_PATH / thumbnailFileNameTemp)) {
            res.status = 404;
            res.set_content("{\"error\":\"Thumbnail file not found.\"}", "application/json");
            return;
        }

        //If file exists, move
        if (!std::filesystem::exists(MEDIA_SERVER_BASE_PATH.string()+"videos/"+videoKey+"/")) {
            std::filesystem::create_directories(MEDIA_SERVER_BASE_PATH.string()+"videos/"+videoKey+"/");
        }
        
        int dotPost = videoFileNameTemp.find_last_of('.');
        std::string extVideoFile = videoFileNameTemp.substr(dotPost);
        
        dotPost = thumbnailFileNameTemp.find_last_of('.');
        std::string extThumbnailFile = thumbnailFileNameTemp.substr(dotPost);

        std::string newPath = MEDIA_SERVER_BASE_PATH.string()+"videos/" + videoKey;

        if(!std::filesystem::exists(newPath)) {
            try {
                std::filesystem::create_directories(newPath);
            } catch (const std::exception &e) {
                res.status = 500;
                res.set_content("{\"error\":\"Failed to create directories\"}", "application/json");
                return;
            }
        }
        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+videoFileNameTemp, 
            newPath + "/video" + extVideoFile
        );
        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+thumbnailFileNameTemp, 
            newPath + "/thumbnail" + extThumbnailFile
        );

        res.set_content("{ \
            \"success\":\"File moved successfully.\", \
            \"videofilename\":\"video"+ extVideoFile +"\",\
            \"thumbnailfilename\":\"/video/thumbnail/"+ videoKey +"/thumbnail"+ extThumbnailFile +"\"\
            }", "application/json");
    });
    srv.Post("/video/move/thumb/temp/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string videoKey = req.matches[1];
        std::string thumbnailFileNameTemp = req.matches[2];

        if (thumbnailFileNameTemp.size() > 0 && !std::filesystem::exists(MEDIA_SERVER_TEMP_PATH / thumbnailFileNameTemp)) {
            res.status = 404;
            res.set_content("{\"error\":\"Thumbnail file not found.\"}", "application/json");
            return;
        }

        int dotPost = thumbnailFileNameTemp.find_last_of('.');
        std::string extThumbnailFile = thumbnailFileNameTemp.substr(dotPost);

        std::string newPath = MEDIA_SERVER_BASE_PATH.string()+"videos/" + videoKey;

        if(!std::filesystem::exists(newPath)) {
            res.status = 404;
            res.set_content("{\"error\":\"Video directory not found.\"}", "application/json");
            return;
        }

        for (auto& i : std::filesystem::directory_iterator(newPath)){
            if (i.is_regular_file() && i.path().filename().string().rfind("thumbnail.", 0) == 0){
                try {
                    std::filesystem::remove(i.path());
                } catch (const std::exception &e) {
                    res.status = 500;
                    res.set_content("{\"error\":\"Failed to remove thumbnail file.\"}", "application/json");
                    return;
                }
            }
        }

        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+thumbnailFileNameTemp, 
            newPath + "/thumbnail" + extThumbnailFile
        );

        res.set_content("{ \
            \"success\":\"File moved successfully.\", \
            \"thumbnailfilename\":\"/video/thumbnail/"+ videoKey +"/thumbnail"+ extThumbnailFile +"\"\
            }", "application/json");
    });
    

    //Get thumbnail from video key
    srv.Get("/video/thumbnail/([^/]+)/([^/]+)", [](const httplib::Request &req, httplib::Response &res){
        std::string videoKey = req.matches[1];
        std::string fileName = req.matches[2];

        std::string fileFolderLoad = MEDIA_SERVER_BASE_PATH.string()+"videos/"+videoKey+"/"+fileName;
        std::ifstream fileLoadOpen(fileFolderLoad, std::ios::ate | std::ios::binary);

        int dotPos = fileName.find_last_of(".");
        std::string ext = fileName.substr(dotPos+1);

        if (!fileLoadOpen.is_open()){
            res.status = 404;
            res.set_content("<h1>This video thumbnail does not exist.</h1>", "text/html");
            return;
        }

        std::streamsize sizeFile = fileLoadOpen.tellg();
        std::vector<char> fileBuffer(sizeFile);

        fileLoadOpen.seekg(0, std::ios::beg);
        fileLoadOpen.read(fileBuffer.data(), sizeFile);

        res.set_header("Access-Control-Allow-Origin", DOMAIN_WEB_SERVER);
        res.set_content(fileBuffer.data(), sizeFile, "image/"+ext);
    });
    //Get videos HLS streaming, send mpegURL to client
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
        std::string newFilePath = MEDIA_SERVER_BASE_PATH.string()+"channels/" + channelId + "/" + typeImage + "_" + channelId + ext;
        std::string newPath = MEDIA_SERVER_BASE_PATH.string()+"channels/" + channelId + "/";
        
        for (auto& i : std::filesystem::directory_iterator(newPath)){
            if (i.is_regular_file() && i.path().filename().string().rfind("cover_"+channelId+".", 0) == 0){
                try {
                    std::filesystem::remove(i.path());
                } catch (const std::exception &e) {
                    res.status = 500;
                    res.set_content("{\"error\":\"Failed to remove thumbnail file.\"}", "application/json");
                    return;
                }
            }
        }

        std::filesystem::rename(
            MEDIA_SERVER_TEMP_PATH.string()+fileName, 
            newFilePath
        );  

        res.set_content("{ \
            \"success\":\"File moved successfully.\", \
            \"imageUrl\":\"/channel/" + channelId + "/image/" + typeImage + "/" + typeImage + "_" + channelId + ext + "\" \
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

    std::cout << "Running..." << std::endl;
    srv.listen("0.0.0.0", 8099);
    return 0;
}