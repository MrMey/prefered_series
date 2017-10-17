class Series:
    """Stores the info regarding the TV shows as seen on Page 1

    Class defining a TV show by :
    - ID in database
    - Title
    - Picture
    - Next episode out"""

    def __init__(self, title, poster, nextepisode, id):
        self.title = title
        self.poster = poster
        self.nextepisode = nextepisode
        self.id = id