import database as db
import model
from api_exception import BadRequestException


def save_submission(submission):
    entity = model.SubmissionItemEntity(submission)
    db.insert(entity)


def save_comment(comment):
    entity = model.CommentItemEntity(comment)
    db.insert(entity)


def retrieve_items(subreddit, from_, to, keyword=None):
    # Validate given parameters
    if subreddit is None or from_ is None or to is None:
        raise BadRequestException("The following query parameters are "
                                  "mandatory: 'subreddit', 'from', 'to'")
    try:
        from_ = int(from_)
        to = int(to)
    except ValueError:
        raise BadRequestException("Query parameters 'from' and 'to' must be "
                                  "valid UNIX timestamps")

    return db.find(subreddit, from_, to, keyword)
