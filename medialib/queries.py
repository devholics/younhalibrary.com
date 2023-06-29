TAG_ORDER_QUERY = '''
SELECT
    A.*,
    num_photo + num_youtubevideo as num_media
FROM
    medialib_tag A
LEFT JOIN
    (
        SELECT
            B.id,
            COUNT(C.photo_id)
                FILTER (
                    WHERE
                        C.photo_id in (
                            SELECT
                                id
                            FROM
                                medialib_photo
                            WHERE
                                public AND license_id IS NOT NULL
                        )
                ) as num_photo
        FROM
            medialib_tag B
        LEFT JOIN
            medialib_photo_tags C
        ON
            B.id = C.tag_id
        GROUP BY
            B.id
    ) D
ON
    A.id = D.id
LEFT JOIN
    (
        SELECT
            E.id,
            COUNT(F.youtubevideo_id)
                FILTER (
                    WHERE
                        F.youtubevideo_id in (
                            SELECT
                                id
                            FROM
                                medialib_youtubevideo
                            WHERE
                                public AND license_id IS NOT NULL
                        )
                ) as num_youtubevideo
        FROM
            medialib_tag E
        LEFT JOIN
            medialib_youtubevideo_tags F
        ON
            E.id = F.tag_id
        GROUP BY
            E.id
    ) G
ON
    A.id = G.id
WHERE
    num_photo + num_youtubevideo > 0
ORDER BY
    num_media DESC
'''

CREATOR_ORDER_QUERY = '''
SELECT
    A.*,
    num_photo + num_youtubevideo as num_media
FROM
    medialib_creator A
INNER JOIN
    (
        SELECT
            B.id,
            COUNT(C.id)
                FILTER (
                    WHERE
                        C.public AND C.license_id IS NOT NULL
                ) as num_photo
        FROM
            medialib_creator B
        LEFT JOIN
            medialib_photo C
        ON
            B.id = C.creator_id
        GROUP BY
            B.id
    ) D
ON
    A.id = D.id
INNER JOIN
    (
        SELECT
            E.id,
            COUNT(F.id)
                FILTER (
                    WHERE
                        F.public AND F.license_id IS NOT NULL
                ) as num_youtubevideo
        FROM
            medialib_creator E
        LEFT JOIN
            medialib_youtubevideo F
        ON
            E.id = F.creator_id
        GROUP BY
            E.id
    ) G
ON
    A.id = G.id
WHERE
    num_photo + num_youtubevideo > 0
ORDER BY
    num_media DESC
'''
