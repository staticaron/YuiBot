anime_query_with_stats = '''
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
                tags {
                    name
                    rank
                    isAdult
                }
            }
        }
    '''

manga_query_with_stats = """
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
            popularity
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

character_query_with_stats = """
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

anime_query_without_stats = '''
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
            }
        }
    '''

manga_query_without_stats = """
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
            popularity
        }
    }
"""

character_query_without_stats = """
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
        }
    }
"""

top_genre_query = """
    query ($genre: [String], $type: MediaType) {
        Page(page: 0, perPage: 50) {
            pageInfo {
            total
            }
            media(genre_in: $genre, sort: SCORE_DESC, type: $type) {
            title {
                english
                romaji
            }
            siteUrl
            meanScore
            }
        }
    }
"""

media_selection_query = """
    query($search:String, $type:MediaType){
        Page(page:0, perPage:5){
            pageInfo{
                total
            }
            media(search:$search, sort:SEARCH_MATCH, type:$type){
                id 
                idMal
                title{
                    english
                    romaji
                }
                siteUrl
                genres
                coverImage{
                    medium
                }
                episodes
                chapters
                status
            }
        }
    }
"""

character_selection_query = """
    query($name:String){
        Page(page:0, perPage:5){
            pageInfo{
                total
            }
            characters(search:$name, sort:SEARCH_MATCH){
                id
                name{
                    full
                    native
                }
                dateOfBirth {
                    year
                    month
                    day
                }
                image{
                    medium
                }
                siteUrl
                favourites
                gender
                age
            }
        } 
    }
"""
