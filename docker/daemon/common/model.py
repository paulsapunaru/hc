from pymongo.son_manipulator import SON


class ItemEntity(SON):
    def __init__(self, item):
        # Take the reddit id
        self["id"] = item.id
        # The subreddit name is case-insensitive, so always store it in
        # lowercase
        self["subreddit"] = item.subreddit.display_name.lower()
        self["created_utc"] = item.created_utc

        # Some items don't have an author
        if not (item.author is None):
            self["author"] = item.author.name


class SubmissionItemEntity(ItemEntity):
    def __init__(self, submission):
        super(SubmissionItemEntity, self).__init__(submission)
        self["type"] = "submission"
        self["title"] = submission.title
        self["text"] = submission.selftext


class CommentItemEntity(ItemEntity):
    def __init__(self, comment):
        super(CommentItemEntity, self).__init__(comment)
        self["type"] = "comment"
        self["body"] = comment.body
