import { useState, useRef, memo } from "react";
import { ROUTES } from "../../base/entries/constants/routes";

const getUserInitials = (name) => {
    if (!name) return "U";
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
};

const formatCommentDate = (date) => {
    if(!date) return '';
    const commentDate = new Date(date);
    
    return commentDate.getDate()
        + '/' + (commentDate.getMonth() + 1)
        + '/' + commentDate.getFullYear();
};

const CommentItem = memo(function CommentItem({ comment, initialData, setTotalComments }) {
    const [comments, setComments] = useState([]);
    const [isReplying, setIsReplying] = useState(false);
    const [totalComments, setTotalRecomments] = useState(comment?.totalRecomments || 0);
    const replyInputRef = useRef(null);
    
    const userAuthor = comment?.userName;
    const userAvatarUrl = comment?.userAvatarUrl;
    const userComment = comment?.commentDescription;

    const loadReplies = () => {
        fetch(ROUTES.loadReplies(comment?.commentId))
            .then((r) => r.json())
            .then((d) => {
                setComments(d);
            });
    };

    const handleReplySubmit = () => {
        if (!replyInputRef.current?.value) return;
        fetch(ROUTES.commentReply(initialData?.videoId, comment?.commentId), {
            method: 'POST',
            body: JSON.stringify({
                comment: replyInputRef.current.value
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((r) => r.json())
            .then((d) => {
                if (d && d?.comments) {
                    setComments((prev) => [...d.comments, ...(prev || [])]);
                    setIsReplying(false);
                    setTotalRecomments((prev) => prev + 1);
                    setTotalComments((prev) => prev + 1);
                }
            });
    };

    const isChild = !!comment?.commentCommentId;
    const avatarBg = isChild ? "bg-emerald-600 border border-emerald-400/30" : "bg-indigo-600 border border-indigo-400/30";

    return (
        <div className="space-y-4">
            {/* Comment Card */}
            <div className="p-6 rounded-2xl bg-white/[0.04] border border-white/5 hover:border-white/10 transition flex items-start gap-4 shadow-sm">
                <div className={`w-11 h-11 rounded-full ${avatarBg} flex items-center justify-center shrink-0 text-xs font-bold text-white shadow-sm`}>
                    {userAvatarUrl ?
                        <img src={userAvatarUrl} className="w-full h-full object-cover rounded-full" alt="" />
                        : getUserInitials(userAuthor)
                    }
                </div>
                <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-3 text-xs">
                        <span className="font-bold text-white text-sm">{userAuthor}</span>
                        <span className="text-gray-400 text-xs">{formatCommentDate(comment?.createdAt)}</span>
                    </div>
                    <p className="text-sm text-gray-200 leading-relaxed">
                        {userComment}
                    </p>
                    
                    {/* Reply Action Button */}
                    <div className="flex items-center gap-6 text-xs text-gray-400 pt-2 border-t border-white/5">
                        <button
                            onClick={() => setIsReplying(!isReplying)}
                            className="hover:text-white transition text-xs font-semibold"
                        >
                            Reply
                        </button>
                    </div>

                    {/* Reply Input Form */}
                    {isReplying && (
                        <div className="mt-3 flex items-start gap-3 pt-4 border-t border-white/5">
                            <div className="w-9 h-9 rounded-full bg-brand/30 border border-brand/40 flex items-center justify-center shrink-0 text-xs font-bold text-white shadow-sm">
                                {initialData?.userAvatarUrl ? (
                                    <img src={initialData.userAvatarUrl} className="w-full h-full object-cover rounded-full" alt="" />
                                ) : (
                                    getUserInitials(initialData?.userName || "U")
                                )}
                            </div>
                            <div className="flex-1 space-y-2">
                                <textarea
                                    ref={replyInputRef}
                                    placeholder="Add a reply..."
                                    rows="2"
                                    className="w-full bg-[#121212] border border-white/10 p-3 rounded-xl text-white placeholder-gray-500 text-xs focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand transition resize-none shadow-inner"
                                ></textarea>
                                <div className="flex justify-end gap-2">
                                    <button
                                        onClick={() => setIsReplying(false)}
                                        className="px-4 py-1.5 text-2xs font-semibold text-gray-300 hover:bg-white/10 rounded-full transition"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={handleReplySubmit}
                                        className="px-4 py-1.5 text-2xs font-semibold text-white bg-brand rounded-full hover:bg-[#772ce8] transition shadow"
                                    >
                                        Reply
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Replies Section */}
            {totalComments > 0 && (
                <div className="ml-6 sm:ml-8 pl-6 sm:pl-8 border-l-2 border-white/10 space-y-4">
                    {/*Load Replies Button*/}
                    {totalComments && comments && totalComments > comments.length ?
                        <div className="flex items-center h-8">
                            <button className="flex items-center gap-2 text-xs font-semibold text-brand hover:text-brand/80 transition py-1.5 px-3.5 rounded-xl bg-brand/5 border border-brand/10 hover:bg-brand/10"
                                onClick={loadReplies}
                            >
                                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                                </svg>
                                <span>View {totalComments} replies</span>
                            </button>
                        </div>
                    : null
                    }

                    {comments.map((reply) => (
                        <CommentItem key={reply?.commentId} comment={reply} initialData={initialData} setTotalComments={setTotalComments} />
                    ))}
                </div>
            )}
        </div>
    );
});

export default function VideoComments({ initialComments, initialData }) {
    const [comments, setComments] = useState(initialComments?.comments || []);
    const [totalComments, setTotalComments] = useState(initialComments?.totalComments)
    const commentInput = useRef(null);
    
    const userName = initialData?.userName;
    const userAvatarUrl = initialData?.userAvatarUrl;

    const handleCommentSubmit = () => {
        if (!commentInput.current?.value) return;
        fetch(ROUTES.commentReply(initialData?.videoId), {
            method: 'POST',
            body: JSON.stringify({
                comment: commentInput.current.value
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((r) => r.json())
            .then((d) => {
                if (d && d?.comments) {
                    setComments((prev) => [...d.comments, ...(prev || [])]);
                    commentInput.current.value = "";
                    setTotalComments((prev) => prev + 1);
                }
            });
    };

    return (
        <div className="space-y-8 pt-6 border-t border-white/10">
            
            <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-white">{totalComments} Comments</h3>
            </div>

            {/*ADD COMMENT INPUT (PADDED CARD CONTAINER)*/}
            <div className="p-6 sm:p-7 rounded-2xl bg-surface/60 border border-white/10 backdrop-blur-md space-y-4 shadow-md">
                <div className="flex items-start gap-4">
                    <div className="w-11 h-11 rounded-full bg-brand/30 border border-brand/40 flex items-center justify-center shrink-0 text-sm font-bold text-white shadow-sm">
                        {userAvatarUrl ?
                            <img src={userAvatarUrl} className="w-full h-full object-cover rounded-full" alt="" />
                            : getUserInitials(userName)
                        }
                    </div>
                    <div className="flex-1 space-y-3">
                        <textarea ref={commentInput} placeholder="Add a public comment..." rows="3" 
                            className="w-full bg-[#121212] border border-white/10 p-4 rounded-xl text-white placeholder-gray-500 text-sm focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand transition resize-none shadow-inner"
                        ></textarea>
                        <div className="flex justify-end gap-3 pt-1">
                            {/*<button className="px-5 py-2 text-xs font-semibold text-gray-300 hover:bg-white/10 rounded-full transition">Cancel</button>*/}
                            <button className="px-6 py-2 text-xs font-semibold text-white bg-brand rounded-full hover:bg-[#772ce8] transition shadow"
                                onClick={handleCommentSubmit}
                            >Comment</button>
                        </div>
                    </div>
                </div>
            </div>

            {/*COMMENTS THREAD LIST*/}
            <div className="space-y-4">
                {comments ? comments.map((comment) => {
                    return (
                        <CommentItem
                            key={comment.commentId}
                            comment={comment}
                            initialData={initialData}
                            setTotalComments={setTotalComments}
                        />
                    );
                }) : null}
            </div>

        </div>
    );
}