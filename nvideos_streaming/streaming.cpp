#include "deps/httplib.h"

int main(int regv, char** regc){
    httplib::Server srv;

    srv.Get("/home", [](const httplib::Request &, httplib::Response &res){
        res.set_content("<h1>still under development</h1>", "text/plain");
    });

    srv.listen("0.0.0.0", 8099);
    return 0;
}