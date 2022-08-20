progress_update_query = """
    mutation($mediaID:Int!, $progress:Int!){
        SaveMediaListEntry(mediaId:$mediaID, progress:$progress){
            mediaId
            media{
                title{
                    english
                    native
                }
            }
        }
    }
"""

recommendation_query = """
    query ($id: Int!) {
        Page(page:0, perPage:5){
            pageInfo {
                total
            }
            recommendations(mediaId: $id, sort: RATING_DESC) {
                id
                rating
                mediaRecommendation {
                    title {
                        english
                        romaji
                    }
                    siteUrl
                    coverImage{
                        medium
                    }
                    description
                    genres
                }
                media{
                    title{
                        english
                        romaji
                    }
                }
            }
        }
    }
"""

media_status_query = """
    mutation($id:Int!, $list:MediaListStatus){
        SaveMediaListEntry(mediaId:$id, status:$list){
            id 
            status
        }
    }
"""

media_rate_query = """
    mutation($mediaID:Int!, $rating:Float){
        SaveMediaListEntry(mediaId:$mediaID, score:$rating){
            media{
                id
                title{
                    english
                    native
                }
            }
        }
    }
"""
