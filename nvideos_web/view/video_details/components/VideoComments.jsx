import { useState, useRef } from "react";
import { ROUTES } from "../../base/entries/constants/routes";

function CommentItem({ comment }) {
    const [userAuthor, setUserAuthor] = useState(comment?.userName);
    const [userAvatarUrl, setUserAvatarUrl] = useState(comment?.userAvatarUrl);
    const [userComment, setUserComment] = useState(comment?.commentDescription);
    const [totalComments, setTotalComments] = useState(comment?.totalRecomments);
    const [comments, setComments] = useState(null);
    const loadMoreDiv = useRef(null);
    
    const formatCommentDate = () => {
        const commentDate = new Date(comment?.createdAt);
        
        return commentDate.getDate()
            + '/' + (commentDate.getMonth() + 1)
            + '/' + commentDate.getFullYear();
    };

    const getUserInitials = (name) => {
        return name.split(' ').map(n => n[0]).join('').toUpperCase();
    };

    const loadReplies = () => {
        fetch(ROUTES.loadReplies(comment?.commentId))
            .then((r) => r.json())
            .then((d) => {
                setComments(d);
                loadMoreDiv.current.classList.add('hidden');
            });
    };

    if (totalComments > 0) {
        return (
            <div className="space-y-3">
                {/*COMMENT ITEM 1 WITH REPLIES*/}

                {/* Parent Comment */}
                <div className="p-6 rounded-2xl bg-white/[0.04] border border-white/5 hover:border-white/10 transition flex items-start gap-4 shadow-sm">
                    <div className="w-11 h-11 rounded-full bg-indigo-600 border border-indigo-400/30 flex items-center justify-center shrink-0 text-xs font-bold text-white shadow-sm">
                        {userAvatarUrl ?
                            <img src={userAvatarUrl} className="w-full h-full object-cover rounded-full" alt="" />
                            : getUserInitials(userAuthor)
                        }
                    </div>
                    <div className="flex-1 space-y-2">
                        <div className="flex items-center gap-3 text-xs">
                            <span className="font-bold text-white text-sm">{userAuthor}</span>
                            <span className="text-gray-400 text-xs">{formatCommentDate()}</span>
                        </div>
                        <p className="text-sm text-gray-200 leading-relaxed">
                            {userComment}
                        </p>
                        <div className="flex items-center gap-6 text-xs text-gray-400 pt-2 border-t border-white/5">
                            <button className="hover:text-white transition text-xs font-semibold">Reply</button>
                        </div>
                    </div>
                </div>

                {/*Replies Wrapper */}
                <div className="ml-6 sm:ml-8 pl-6 sm:pl-8 border-l-2 border-white/10 space-y-4">
                    
                    {/*Load Replies Button*/}
                    <div ref={loadMoreDiv}  className="flex items-center h-8">
                        <button className="flex items-center gap-2 text-xs font-semibold text-brand hover:text-brand/80 transition py-1.5 px-3.5 rounded-xl bg-brand/5 border border-brand/10 hover:bg-brand/10"
                            onClick={loadReplies}
                        >
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                            </svg>
                            <span>View {comment?.totalComments} replies</span>
                        </button>
                    </div>

                    {comments ?
                        comments.map((comment) => {
                            return (
                                <CommentItem key={comment?.commentId} comment={comment} />
                            );
                        }) : null
                    }

                    {/*COMMENTS CUTTED*/}
                    
                </div>
            </div>
        );
    }

    return (        
        <div className="p-6 rounded-2xl bg-white/[0.04] border border-white/5 hover:border-white/10 transition flex items-start gap-4 shadow-sm">
            {/* COMMENT ITEM 2 */}
            <div className="w-11 h-11 rounded-full bg-emerald-600 border border-emerald-400/30 flex items-center justify-center shrink-0 text-xs font-bold text-white shadow-sm">
                {userAvatarUrl ?
                    <img src={userAvatarUrl} className="w-full h-full object-cover rounded-full" alt="" />
                    : getUserInitials(userAuthor)
                }
            </div>
            <div className="flex-1 space-y-2">
                <div className="flex items-center gap-3 text-xs">
                    <span className="font-bold text-white text-sm">{userAuthor}</span>
                    <span className="text-gray-400 text-xs">{formatCommentDate()}</span>
                </div>
                <p className="text-sm text-gray-200 leading-relaxed">
                    {userComment}
                </p>
                <div className="flex items-center gap-6 text-xs text-gray-400 pt-2 border-t border-white/5">
                    <button className="hover:text-white transition text-xs font-semibold">Reply</button>
                </div>
            </div>
        </div>
    );
};

export default function VideoComments({ initialComments }) {
    
    return (
        <div className="space-y-8 pt-6 border-t border-white/10">
            
            <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-white">248 Comments</h3>
                <button className="flex items-center gap-2 text-xs font-semibold text-gray-300 hover:text-white transition px-4 py-2 rounded-xl bg-white/5 border border-white/10">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h10M4 18h7"/>
                    </svg>
                    <span>Sort by</span>
                </button>
            </div>

            {/*ADD COMMENT INPUT (PADDED CARD CONTAINER)*/}
            <div className="p-6 sm:p-7 rounded-2xl bg-surface/60 border border-white/10 backdrop-blur-md space-y-4 shadow-md">
                <div className="flex items-start gap-4">
                    <div className="w-11 h-11 rounded-full bg-brand/30 border border-brand/40 flex items-center justify-center shrink-0 text-sm font-bold text-white shadow-sm">
                        U
                    </div>
                    <div className="flex-1 space-y-3">
                        <textarea placeholder="Add a public comment..." rows="3" 
                            className="w-full bg-[#121212] border border-white/10 p-4 rounded-xl text-white placeholder-gray-500 text-sm focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand transition resize-none shadow-inner"></textarea>
                        <div className="flex justify-end gap-3 pt-1">
                            <button className="px-5 py-2 text-xs font-semibold text-gray-300 hover:bg-white/10 rounded-full transition">Cancel</button>
                            <button className="px-6 py-2 text-xs font-semibold text-white bg-brand rounded-full hover:bg-[#772ce8] transition shadow">Comment</button>
                        </div>
                    </div>
                </div>
            </div>

            {/*COMMENTS THREAD LIST*/}
            <div className="space-y-4">
                {initialComments && initialComments.comments ? initialComments?.comments.map((comment) => {
                    return (
                        <CommentItem key={comment.commentId} comment={comment} />
                    );
                }) : null}
            </div>

        </div>
    );

};