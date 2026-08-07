# FLASK
from flask import Blueprint, render_template, request as flaskRequest, session

# SERVICE
from nvideos_web.services.video.service import VideoService, Video

# DECORATOR
from nvideos_web.view.endpoint_decorators import loginRequired

videoDetailsBp = Blueprint(
    "video_details", __name__,
    static_folder="static", static_url_path="/video_details/static",
    template_folder="template"
)

@videoDetailsBp.route("/video/<video_key>")
@loginRequired
def video_detail(video_key):
    #TODO: Select video to vd
    renderTemplate = render_template("video_detail.html", vd=None)
    return renderTemplate

@videoDetailsBp.route("/video/create", methods=["GET", "POST"])
@loginRequired
def video_detail_create():
    if flaskRequest.method == "POST":
        form: dict[str, str] = flaskRequest.form
        vSrv: VideoService = VideoService(userId=session.get("userId"))
        
        #TODO: check for viewkey in mediaserver, if not there, throw error
        if not form.get('videoKey'):
            return render_template("base/error.html", error="Video was not uploaded. Please try again.")  

        videoTags: list[str] | None = str(form.get("videoTags")).split(',') if form.get("videoTags") else None
        channelIdStr: str | None = form.get("channelId") #Pyrigthly
        channelId: int | None = int(channelIdStr) if channelIdStr else None

        videoCreated: Video = vSrv.translateVideoPermission(form.get("videoPermission"))\
        .fillInputData(
            videoTitle=form.get("videoTitle"),
            videoDescription=form.get("videoDescription"),
            videoTags=videoTags,
            channelId=channelId,
            videoKey=form.get("videoKey")
        ).createNewVideo()

    return render_template("video_details_edit.html")

@videoDetailsBp.route("/video/<video_key>/edit")
@loginRequired
def video_detail_edit(video_key: str):
    return render_template("video_details_edit.html", vd=None)