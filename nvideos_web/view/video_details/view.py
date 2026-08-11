# FLASK
from flask import (
    Blueprint, render_template, 
    request as flaskRequest, 
    session, jsonify
)
import flask

# SERVICE
from nvideos_web.services.video.service import VideoService, Video

# DECORATOR
from nvideos_web.view.endpoint_decorators import loginRequired, channelRequired, authKeyNeeded

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
        
        #TODO: Check for video temp name in mediaserver ? It's necessary ?
        if not form.get('videoTempFilename'):
            return render_template("base/error.html", error="Video was not uploaded. Please try again.")  

        videoTags: list[str] | None = [i.strip()for i in str(form.get("videoTags")).split(',')] if form.get("videoTags") else None
        videoCreated: Video | None = None
        try:
            #TODO: Encepsulate this in the future, along with other views/services usage.
            videoCreated = vSrv.translateVideoPermission(form.get("videoPermission"))\
            .fillInputData(
                videoTitle=form.get("videoTitle"),
                videoDescription=form.get("videoDescription"),
                videoTags=videoTags,
                videoViewCount=0,
                videoKey=form.get("videoKey")
            ).checkInputDataIsValid().createNewVideo()

            videoCreated = vSrv.generateCheckVideoKey().moveTempFilesToNewPath(
                videoTempFilename=form.get("videoTempFilename"),
                videoThumbnailTempFilename=form.get("videoThumbTempFilename")
            ).fillInputData().updateVideoById(
                videoCreated.videoId
            )

            #Process redis to start converting video.
            vSrv.processEnqueuedMessagesRedis()

            #I could redirect but I will keep it simple for now.
            return render_template("video/video_details_edit.html", vd=videoCreated)
        except Exception as e:
            if videoCreated:
                _ = vSrv.deleteVideoById(videoId=videoCreated.videoId)

            return render_template("base/error.html", error=str(e))

    return render_template("video/video_details_edit.html")

@videoDetailsBp.route("/video/list", methods=["GET"])
@loginRequired
@channelRequired
def video_list():
    return render_template("video/video_list.html")

@videoDetailsBp.route("/video/<string:video_key>/edit", methods=["GET", "POST"])
@loginRequired
@channelRequired
def video_detail_edit(video_key: str):
    vSrv: VideoService = VideoService(
        userId=session.get("userId"),
        channelId=session.get("channelId")
    )

    vd: Video | None = vSrv.selectByVideoKey(video_key)
    if not vd:
        return render_template("base/error.html", error="Video not found")

    if flaskRequest.method == "POST":
        try:
            form: dict[str, str] = flaskRequest.form
            videoTags: list[str] | None = [i.strip()for i in str(form.get("videoTags")).split(',')] if form.get("videoTags") else None
            thumbnailTempFile: str | None = form.get("videoThumbTempFilename")

            #I could do it on one swipe, but I will keep it in two calls to DB for now.
            vd = vSrv.translateVideoPermission(form.get("videoPermission")) \
            .fillInputData(
                videoTitle=form.get("videoTitle"),
                videoDescription=form.get("videoDescription"),
                videoTags=videoTags
            ).checkInputDataIsValid().updateVideoById(vd.videoId)

            if thumbnailTempFile and vd.videoThumbUrl != thumbnailTempFile:
                vd = vSrv.moveTempThumbToVideoPath(
                    vd.videoKey, 
                    thumbnailTempFile
                ).fillInputData().updateVideoById(vd.videoId)

            return render_template("video/video_details_edit.html", vd=vd)

        except Exception as e:
            return render_template("base/error.html", error=str(e))

    return render_template("video/video_details_edit.html", vd=vd)

@videoDetailsBp.route("/video/<string:video_key>")
@loginRequired
@channelRequired
def video_detail(video_key: str):
    #TODO: Select video to vd
    renderTemplate = render_template("video/video_detail.html", vd=None)
    return renderTemplate

@videoDetailsBp.route("/video/status/<string:video_key>", methods=["GET"])
@loginRequired
@channelRequired
def video_status(video_key: str):
    try:
        percent: str = VideoService().checkVideoProcessingStatus(video_key)
        if percent:
            return jsonify({"percent": percent})
        return jsonify({"percent": None})
    except Exception as e:
        #LOG: logging.exception(e)
        return jsonify({"error": True})

@videoDetailsBp.route("/video/processing/finished/<string:video_key>/<int:time_duration>", methods=["GET", "POST"])
@authKeyNeeded
def video_processing_finished(video_key: str, time_duration: int):
    #TODO: I will keep it simple for now.
    VideoService().finishedVideoProcessing(video_key, time_duration)
    return jsonify({"success": True})
