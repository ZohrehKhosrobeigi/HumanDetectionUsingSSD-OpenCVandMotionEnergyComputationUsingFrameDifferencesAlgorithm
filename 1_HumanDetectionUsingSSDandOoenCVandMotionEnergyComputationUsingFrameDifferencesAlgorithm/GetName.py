class GetName():
    def getName(self,file):
        tmp=file.split("/")
        tmp=tmp[1].split("_")
        self.player1=tmp[0]

        self.session=tmp[1]

        return self.player1,self.session