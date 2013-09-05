from collective.rcse.page.controller.group_base import BaseView


class AudiosView(BaseView):
    """A filterable timeline"""
    filter_type = ["collective.rcse.audio"]

    def getAudios(self):
        results = self.get_content(batch=False)
        audios = []
        for result in results:
            obj = result.getObject()
            audio = {}
            audio["src"] = obj.absolute_url() + '/@@download/file/'
            audio["src"] += obj.file.filename.encode('utf-8')
            audio["title"] = obj.title
            audio["description"] = obj.description
            audio["mimetype"] = obj.file.contentType
            audio["duration"] = ""
            audios.append(audio)
        return audios
