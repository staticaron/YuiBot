list_query = """
    query($id:Int!, $status:MediaListStatus, $media:MediaType){
        MediaListCollection(userId:$id, type:$media, status:$status, sort:UPDATED_TIME_DESC){
            lists{
                name
                entries{
                    media{
                        title{
                            english
                            romaji
                        }
                        siteUrl
                        episodes
                        chapters
                    }
                    progress
                }
                isCustomList
            }
            user{
                avatar{
                    medium
                }
            }
        }
    }
"""
