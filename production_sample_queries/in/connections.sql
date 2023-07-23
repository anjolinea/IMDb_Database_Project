WITH RECURSIVE FollowersRecursive AS (
    SELECT Follows.userID1 AS follower,
        Follows.userID2 AS follower_of_follower, 
        0 AS level
    FROM Follows
    WHERE Follows.userID1 = 'jenniferhernandez64'
    UNION ALL
    SELECT FollowersRecursive.follower,
        Follows.userID2, 
        FollowersRecursive.level + 1
    FROM Follows
    JOIN FollowersRecursive ON 
        Follows.userID1 = FollowersRecursive.follower_of_follower
    WHERE FollowersRecursive.level < 2
)
SELECT follower_of_follower AS follower, MIN(level) AS level
FROM FollowersRecursive
GROUP BY follower_of_follower
LIMIT 10;