# FLASK
from flask import Blueprint, render_template, request as flaskRequest, session

# SERVICE
from nvideos_web.services.video.service import VideoService, Video

# DECORATOR
from nvideos_web.view.endpoint_decorators import loginRequired, channelRequired

videoDetailsBp = Blueprint(
    "video_details", __name__,
    static_folder="static", static_url_path="/video_details/static",
    template_folder="template"
)

@videoDetailsBp.route("/video/create", methods=["GET", "POST"])
@loginRequired
@channelRequired
def video_detail_create():
    if flaskRequest.method == "POST":
        form: dict[str, str] = flaskRequest.form

        vSrv: VideoService = VideoService(
            userId=session.get("userId"),
            channelId=session.get("channelId")
        )
        
        #TODO: check for viewkey in mediaserver, if not there, throw error
        if not form.get('videoKey'):
            return render_template("base/error.html", error="Video was not uploaded. Please try again.")  

        videoTags: list[str] | None = str(form.get("videoTags")).split(',') if form.get("videoTags") else None
        videoCreated: Video | None = None
        try:
            #TODO: Encepsulate this in the future, along with other views/services usage.
            videoCreated = vSrv.translateVideoPermission(form.get("videoPermission"))\
            .fillInputData(
                videoTitle=form.get("videoTitle"),
                videoDescription=form.get("videoDescription"),
                videoTags=videoTags,
                videoKey=form.get("videoKey")
            ).checkInputDataIsValid().createNewVideo()

            _ = vSrv.generateCheckVideoKey().moveTempFilesToNewPath(
                videoTempFilename=form.get("videoTempFilename"),
                videoThumbnailTempFilename=form.get("videoThumbnailTempFilename"),
                channelId=None
            ).fillInputData().updateVideoById(
                videoCreated.videoId
            )
                
            return render_template("base/error.html", error=str(e))
        except Exception as e:
            if videoCreated:
                _ = vSrv.deleteVideoById(videoId=videoCreated.videoId)

            return render_template("base/error.html", error=str(e))

    return render_template("video_details_edit.html")

@videoDetailsBp.route("/video/list", methods=["GET"])
@loginRequired
@channelRequired
def video_list():
    return render_template("video_list.html")

@videoDetailsBp.route("/video/<video_key>/edit")
@loginRequired
@channelRequired
def video_detail_edit(video_key: str):
    return render_template("video_details_edit.html", vd=None)

@videoDetailsBp.route("/video/<video_key>")
@loginRequired
@channelRequired
def video_detail(video_key):
    #TODO: Select video to vd
    renderTemplate = render_template("video_detail.html", vd=None)
    return renderTemplate
