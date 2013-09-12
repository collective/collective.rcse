from plone.app.search import browser

#THIS IS A PATCH BECAUSE IT JUST DOESN T WORK ...
class Search(browser.Search):
    def filter_query(self, query):
        text = self.request.form.get('SearchableText', None)
        if text and type(text) is unicode:
            self.request.form['SearchableText'] = text.encode('utf-8')
        return super(Search, self).filter_query(query)

