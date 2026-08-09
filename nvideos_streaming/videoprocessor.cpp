#include <sw/redis++/redis++.h>

#include "deps/json.hpp"

#include <cstdio>
#include <iostream>
#include <string>
#include <filesystem>
#include <unistd.h>
#include <threads.h>
#include <wait.h>

#define REDIS_ADDRESS "tcp://localhost:6379"

std::filesystem::path MEDIA_SERVER_BASE_PATH = "/usr/media_server/";

double get_video_time_duration(std::string videoKey, std::string videoFile){
    std::string videoFilePath = MEDIA_SERVER_BASE_PATH.string() + "videos/" + videoKey + "/" + videoFile;
    if (!std::filesystem::exists(videoFilePath)){
        std::cerr << "ERROR: Video file does not exist: " << std::endl;
        exit(1);
    }
    
    int fds[2];
    pipe(fds);

    int pid = fork();
    if (pid < 0){
        close(fds[0]);
        close(fds[1]);
        std::cerr << "ERROR ON FORK" << std::endl;
        exit(1);
    }

    if (pid == 0){
        dup2(fds[1], STDOUT_FILENO);

        close(fds[0]);
        close(fds[1]);

        const char *args[] = {
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            "/usr/media_server/videos/aaa/video.webm",
            nullptr
        };

        char* const* c = const_cast<char* const*>(args);
        execvp("ffprobe", c);

        //After execvp nothing is called.
        std::cerr << "======> ERROR ON FFPROBE EXECVP" << std::endl;
        exit(1);
    }
    close(fds[1]);

    double totalVideoTime = 0.0;
    char c[256];
    FILE* f = fdopen(fds[0], "r");

    if (!f){
        std::cerr << "ERROR ON FDOPEN" << std::endl;
        exit(1);
    }

    while (fgets(c, sizeof(c), f)){
        try{
            totalVideoTime = std::stod(c);
        } catch(std::exception &e){
            std::cerr << "ERROR ON STOD" << e.what() << std::endl;
            exit(1);
        };
    }
    
    fclose(f);
    waitpid(pid, nullptr, 0);
    return totalVideoTime;
}

void process_video_file(std::string videoKey, std::string videoFile, sw::redis::Redis redis) {
    double totalDuration = get_video_time_duration(videoKey, videoFile);
    std::string videoFilePath = MEDIA_SERVER_BASE_PATH.string() + "videos/" + videoKey + "/" + videoFile;

    if (totalDuration == 0){
        std::cerr << "ERROR ON GET VIDEO TIME DURATION" << std::endl;
        exit(1);
    }

    if (!std::filesystem::exists(videoFilePath)){
        std::cerr << "ERROR: Video file does not exist: " << std::endl;
        exit(1);
    }

    int fds[2];
    pipe(fds);
   
    int pid = fork();

    if (pid < 0){
        close(fds[0]);
        close(fds[1]);
        exit(1);
    }

    if (pid == 0){
        dup2(fds[1], STDOUT_FILENO);
        
        //Closing fds in the child process
        close(fds[1]);
        close(fds[0]);


        const char *args[] = {
            "ffmpeg",
            "-i", "/usr/media_server/videos/aaa/video.webm",
            "-vf",
            "scale=-2:720",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "26",
            "-maxrate", "1500k",
            "-bufsize", "3000k",
            "-c:a", "aac",
            "-b:a", "96k",
            "-g", "60",
            "-keyint_min", "60",
            "-sc_threshold", "0",
            "-progress", "pipe:1",
            "-hls_time", "6",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", "/usr/media_server/videos/aaa/playlist%d.ts", "/usr/media_server/videos/aaa/playlist.m3u8",
            nullptr
        };

        char* const* args_exec = const_cast<char* const*>(args);
        execvp("ffmpeg", args_exec);
        
        //After execvp nothing is called.
        std::cerr << "======> ERROR ON FFMPEG EXECVP" << std::endl;
        exit(1);
    }
    close(fds[1]);

    char c[256];
    FILE* f = fdopen(fds[0], "r");
    
    if (!f){
        std::cerr << "ERROR ON fdopen" << std::endl;
        exit(1);
    }

    while (fgets(c, sizeof(c), f)){
        std::string cc(c);
        if (cc.find("out_time_ms=") != std::string::npos){
            double currentTime = std::stod(cc.substr(
                cc.find_last_of("=") + 1,
                cc.size() - cc.find_last_of("=")
            ));
            int currentPercent = round(((currentTime/1000000.0) / totalDuration) * 100);
            redis.set("video:processing:" + videoKey, std::to_string(currentPercent));
        }
    }

    fclose(f);
    waitpid(pid, nullptr, 0);
}

int main(int argc, char *argv[]) {
    /*std::thread t(process_video_file, "aaa", "video.webm");
    
    if (t.joinable()){
        t.join();
    }

    return 0;*/

    sw::redis::Redis redis = sw::redis::Redis(REDIS_ADDRESS);

    auto sub = redis.subscriber();

    sub.on_message([&redis](std::string channel, std::string msg){ 
        nlohmann::json j = nlohmann::json::parse(msg);
        if(j.contains("videoKey") && j.contains("videoFilename")){
            //std::thread t(process_video_file, 
            // j["videoKey"].get<std::string>(), 
            // j["videoFilename"].get<std::string>(),
            // redis
            //);
            std::cout << j["videoKey"] << j["videoFilename"] << std::endl;
        }
    });
    sub.subscribe("video_upload");
    
    while(1){
        sub.consume();
    }
}