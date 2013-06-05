from collective.rcse.page.common.person import CreatorMemberInfoView


class VCardView(CreatorMemberInfoView):
    """VCard view helper to display member info"""

    def __call__(self):
        self.update()
        return self.index()
