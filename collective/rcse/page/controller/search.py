from plone.app.search import browser


#THIS IS A PATCH BECAUSE IT JUST DOESN'T WORK ...
# => I AGREE
class Search(browser.Search):
    def filter_query(self, query):
        text = self.request.form.get('SearchableText', None)
        if text and type(text) is unicode:
            self.request.form['SearchableText'] = text.encode('utf-8')
        sort_order = self.request.form.get('sort_order', None)
        if sort_order and type(sort_order) is unicode:
            self.request.form['sort_order'] = sort_order.encode('utf-8')
        portal_type = self.request.form.get('portal_type', None)
        if portal_type == 'collective.rcse.group':
            self.request.form['portal_type'] = ['collective.rcse.group',
                                                'collective.rcse.proxygroup']
        return super(Search, self).filter_query(query)
