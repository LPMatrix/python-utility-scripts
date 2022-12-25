import instaloader

# Enter your Instagram username and password
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

# Create an Instaloader object and log in to Instagram
L = instaloader.Instaloader()
L.login(USERNAME, PASSWORD)

# Get your own profile
profile = instaloader.Profile.from_username(L.context, USERNAME)

# Get a list of users you are following
following = profile.get_followers()

# Filter the list of users by those that have never interacted with any of your posts and do not follow you
non_interacting_following = []
for user in following:
    # Get a list of your posts
    posts = profile.get_posts()

    # Check if the user has ever liked or commented on any of your posts
    has_interacted = False
    for post in posts:
        likes = post.get_likes()
        comments = post.get_comments()
        if user in likes or user in comments:
            has_interacted = True
            break

    # Check if the user follows you
    follows_you = user.follows_viewer

    # Add the user to the list if they have never interacted with any of your posts and do not follow you
    if not has_interacted and not follows_you:
        non_interacting_following.append(user)

# Set the number of unfollows per batch
BATCH_SIZE = 20

# Unfollow the users in batches
for i in range(0, len(non_interacting_following), BATCH_SIZE):
    batch = non_interacting_following[i:i+BATCH_SIZE]
    for user in batch:
        L.unfollow(user)
        print(f"Successfully unfollowed {user.username}!")

    # Wait for 10 seconds between batches to avoid exceeding rate limits
    time.sleep(10)