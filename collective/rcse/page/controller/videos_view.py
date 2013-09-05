from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView


class VideosView(BaseView):
    """A filterable timeline"""
    filter_type = ["collective.rcse.video"]

    def getVideos(self):
        results = self.get_content(batch=False)
        videos = []
        for result in results:
            obj = result.getObject()
            video = {}
            video["src"] = obj.absolute_url() + '/@@download/file/'
            video["src"] += obj.file.filename.encode('utf-8')
            video["title"] = obj.title
            video["description"] = obj.description
            video["mimetype"] = obj.file.contentType
            videos.append(video)
        return videos


class NavigationRootVideosView(VideosView, NavigationRootBaseView):
    def update(self):
        VideosView.update(self)
        NavigationRootBaseView.update(self)