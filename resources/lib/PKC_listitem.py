# -*- coding: utf-8 -*-
###############################################################################
import logging

from xbmcgui import ListItem

###############################################################################
log = logging.getLogger("PLEX."+__name__)

###############################################################################


def convert_PKC_to_listitem(PKC_listitem):
    """
    Insert a PKC_listitem and you will receive a valid XBMC listitem
    """
    listitem = ListItem()
    for func, args in PKC_listitem.data.items():
        if isinstance(args, list):
            for arg in args:
                getattr(listitem, func)(*arg)
        elif isinstance(args, dict):
            for arg in args.items():
                getattr(listitem, func)(*arg)
        elif args is None:
            continue
        else:
            getattr(listitem, func)(args)
    return listitem


class PKC_ListItem(object):
    """
    Imitates xbmcgui.ListItem and its functions. Pass along PKC_Listitem().data
    when pickling!

    WARNING: set/get path only via setPath and getPath! (not getProperty)
    """
    def __init__(self, label=None, label2=None, path=None):
        self.data = {
            'addStreamInfo': [],  # (type, values: dict { label: value })
            'setArt': [],  # dict: { label: value }
            'setInfo': {},  # type: infoLabel (dict { label: value })
            'setLabel': label,  # string
            'setLabel2': label2,  # string
            'setPath': path,  # string
            'setProperty': {},  # (key, value)
            'setSubtitles': [],  # string
        }

    def addContextMenuItems(self, items, replaceItems):
        """
        Adds item(s) to the context menu for media lists.

        items : list - [(label, action,)*] A list of tuples consisting of label
        and action pairs.
            - label : string or unicode - item's label.
            - action : string or unicode - any built-in function to perform.
        replaceItes : [opt] bool - True=only your items will show/False=your
        items will be amdded to context menu(Default).

        List  of functions - http://kodi.wiki/view/List_of_Built_In_Functions

         *Note, You can use the above as keywords for arguments and skip
         certain optional arguments.

         Once you use a keyword, all following arguments require the keyword.
        """
        raise NotImplementedError

    def addStreamInfo(self, type, values):
        """
        Add a stream with details.
        type : string - type of stream(video/audio/subtitle).
        values : dictionary - pairs of { label: value }.

        - Video Values:
            - codec : string (h264)
            - aspect : float (1.78)
            - width : integer (1280)
            - height : integer (720)
            - duration : integer (seconds)
        - Audio Values:
            - codec : string (dts)
            - language : string (en)
            - channels : integer (2)
        - Subtitle Values:
            - language : string (en)
        """
        self.data['addStreamInfo'].append((type, values))

    def getLabel(self):
        """
        Returns the listitem label
        """
        return self.data['setLabel']

    def getLabel2(self):
        """
        Returns the listitem label.
        """
        return self.data['setLabel2']

    def getMusicInfoTag(self):
        """
        returns the MusicInfoTag for this item.
        """
        raise NotImplementedError

    def getProperty(self, key):
        """
        Returns a listitem property as a string, similar to an infolabel.
         key : string - property name.
         *Note, Key is NOT case sensitive.

         You can use the above as keywords for arguments and skip certain
         optional arguments.

         Once you use a keyword, all following arguments require the keyword.
        """
        return self.data['setProperty'].get(key)

    def getVideoInfoTag(self):
        """
        returns the VideoInfoTag for this item
        """
        raise NotImplementedError

    def getdescription(self):
        """
        Returns the description of this PlayListItem
        """
        raise NotImplementedError

    def getduration(self):
        """
        Returns the duration of this PlayListItem
        """
        raise NotImplementedError

    def getfilename(self):
        """
        Returns the filename of this PlayListItem.
        """
        raise NotImplementedError

    def isSelected(self):
        """
        Returns the listitem's selected status
        """
        raise NotImplementedError

    def select(self):
        """
        Sets the listitem's selected status.
        selected : bool - True=selected/False=not selected
        """
        raise NotImplementedError

    def setArt(self, values):
        """
        Sets the listitem's art
        values : dictionary - pairs of { label: value }.

        Some default art values (any string possible):
            - thumb : string - image filename
            - poster : string - image filename
            - banner : string - image filename
            - fanart : string - image filename
            - clearart : string - image filename
            - clearlogo : string - image filename
            - landscape : string - image filename
            - icon : string - image filename
        """
        self.data['setArt'].append(values)

    def setContentLookup(self, enable):
        """
        Enable or disable content lookup for item.

        If disabled, HEAD requests to e.g determine mime type will not be sent.

        enable : bool
        """
        raise NotImplementedError

    def setInfo(self, type, infoLabels):
        """
        type : string - type of media(video/music/pictures).

        infoLabels : dictionary - pairs of { label: value }. *Note, To set
        pictures exif info, prepend 'exif:' to the label. Exif values must be
        passed as strings, separate value pairs with a comma. (eg.
        {'exif:resolution': '720,480'}

        See CPictureInfoTag::TranslateString in PictureInfoTag.cpp for valid
        strings. You can use the above as keywords for arguments and skip
        certain optional arguments.

        Once you use a keyword, all following arguments require the keyword.

        - General Values that apply to all types:
            - count : integer (12) - can be used to store an id for later, or
              for sorting purposes
            - size : long (1024) - size in bytes
            - date : string (d.m.Y / 01.01.2009) - file date

        - Video Values:
            - genre : string (Comedy)
            - year : integer (2009)
            - episode : integer (4)
            - season : integer (1)
            - top250 : integer (192)
            - tracknumber : integer (3)
            - rating : float (6.4) - range is 0..10
            - userrating : integer (9) - range is 1..10
            - watched : depreciated - use playcount instead
            - playcount : integer (2) - number of times this item has been
              played
            - overlay : integer (2) - range is 0..8. See GUIListItem.h for
              values
            - cast : list (["Michal C. Hall","Jennifer Carpenter"]) - if
              provided a list of tuples cast will be interpreted as castandrole
            - castandrole : list of tuples ([("Michael C.
              Hall","Dexter"),("Jennifer Carpenter","Debra")])
            - director : string (Dagur Kari)
            - mpaa : string (PG-13)
            - plot : string (Long Description)
            - plotoutline : string (Short Description)
            - title : string (Big Fan)
            - originaltitle : string (Big Fan)
            - sorttitle : string (Big Fan)
            - duration : integer (245) - duration in seconds
            - studio : string (Warner Bros.)
            - tagline : string (An awesome movie) - short description of movie
            - writer : string (Robert D. Siegel)
            - tvshowtitle : string (Heroes)
            - premiered : string (2005-03-04)
            - status : string (Continuing) - status of a TVshow
            - code : string (tt0110293) - IMDb code
            - aired : string (2008-12-07)
            - credits : string (Andy Kaufman) - writing credits
            - lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
            - album : string (The Joshua Tree)
            - artist : list (['U2'])
            - votes : string (12345 votes)
            - trailer : string (/home/user/trailer.avi)
            - dateadded : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
            - mediatype : string - "video", "movie", "tvshow", "season",
              "episode" or "musicvideo"

        - Music Values:
            - tracknumber : integer (8)
            - discnumber : integer (2)
            - duration : integer (245) - duration in seconds
            - year : integer (1998)
            - genre : string (Rock)
            - album : string (Pulse)
            - artist : string (Muse)
            - title : string (American Pie)
            - rating : string (3) - single character between 0 and 5
            - lyrics : string (On a dark desert highway...)
            - playcount : integer (2) - number of times this item has been
              played
            - lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)

        - Picture Values:
            - title : string (In the last summer-1)
            - picturepath : string (/home/username/pictures/img001.jpg)
            - exif : string (See CPictureInfoTag::TranslateString in
              PictureInfoTag.cpp for valid strings)
        """
        self.data['setInfo'][type] = infoLabels

    def setLabel(self, label):
        """
        Sets the listitem's label.
        label : string or unicode - text string.
        """
        self.data['setLabel'] = label

    def setLabel2(self, label):
        """
        Sets the listitem's label2.
        label : string or unicode - text string.
        """
        self.data['setLabel2'] = label

    def setMimeType(self, mimetype):
        """
        Sets the listitem's mimetype if known.
        mimetype : string or unicode - mimetype.

        If known prehand, this can (but does not have to) avoid HEAD requests
        being sent to HTTP servers to figure out file type.
        """
        raise NotImplementedError

    def setPath(self, path):
        """
        Sets the listitem's path.
        path : string or unicode - path, activated when item is clicked.

         *Note, You can use the above as keywords for arguments.
        """
        self.data['setPath'] = path

    def setProperty(self, key, value):
        """
        Sets a listitem property, similar to an infolabel.
            key : string - property name.
            value : string or unicode - value of property.
        *Note, Key is NOT case sensitive.

        You can use the above as keywords for arguments and skip certain
        optional arguments. Once you use a keyword, all following arguments
        require the keyword.

        Some of these are treated internally by XBMC, such as the
        'StartOffset' property, which is the offset in seconds at which to
        start playback of an item. Others may be used in the skin to add extra
        information, such as 'WatchedCount' for tvshow items
        """
        self.data['setProperty'][key] = value

    def setSubtitles(self, subtitles):
        """
        Sets subtitles for this listitem. Pass in a list of filepaths

        example:
            - listitem.setSubtitles(['special://temp/example.srt',
              'http://example.com/example.srt' ])
        """
        self.data['setSubtitles'].extend(([subtitles],))
