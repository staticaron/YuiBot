anime_query = '''
        query ($search : String) { 
            Media (search:$search, type: ANIME, sort:SEARCH_MATCH) { 
                id
                title { 
                    romaji
                    english
                    native
                }
                description(asHtml: false)
                isAdult
                trailer{
                    id
                    site
                }
                siteUrl
                genres
                episodes
                duration
                status
                coverImage {
                    large
                }
                startDate{
                    day
                    month
                    year
                }
                averageScore
                meanScore
                favourites
                format
                studios{
                    nodes{
                        name
                        siteUrl
                    }
                }

                mediaListEntry{
                    status
                    progress
                    media{
                        episodes
                    }
                    score
                }
                isFavourite
            }
        }
    '''

manga_query = """
    query ($search : String) { 
        Media (search:$search, type: MANGA, sort:SEARCH_MATCH) { 
            id
            title {
                romaji
                english
                native
            }
            description(asHtml: false)
            isAdult
            trailer{
                id
                site
            }
            siteUrl
            genres
            chapters
            volumes
            status
            coverImage {
                large
            }
            startDate{
                day
                month
                year
            }
            averageScore
            meanScore
            favourites
            format
            studios(sort:SEARCH_MATCH){
                nodes{
                    name
                    siteUrl
                }
            }

            isFavourite
            mediaListEntry{
                status
                progress
                media{
                    chapters
                }
                score
            }
        }
    }
"""

character_query = """
    query($search : String){
        Character(search :$search, sort:SEARCH_MATCH){
            id
            name{
                full
                native
                alternative
            }
            image{
                medium
            }
            description(asHtml : false)
            gender
            dateOfBirth{
                day
                month
                year
            }
            media(sort:POPULARITY_DESC){
                nodes{
                    title{
                        english
                        romaji
                    }
                    siteUrl
                }
            }
            age
            bloodType
            siteUrl
            favourites

            isFavourite
        }
    }
"""