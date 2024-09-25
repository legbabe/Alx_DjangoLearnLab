## API Endpoints

### Posts
- `POST /api/posts/`: Create a new post.
- `GET /api/posts/`: Retrieve a list of posts with pagination.
- `GET /api/posts/{id}/`: Retrieve a specific post with its comments.
- `PUT /api/posts/{id}/`: Update an existing post (only if you are the author).
- `DELETE /api/posts/{id}/`: Delete a post (only if you are the author).

### Comments
- `POST /api/comments/`: Create a new comment.
- `GET /api/comments/`: Retrieve a list of comments.
- `GET /api/comments/{id}/`: Retrieve a specific comment.
- `PUT /api/comments/{id}/`: Update an existing comment (only if you are the author).
- `DELETE /api/comments/{id}/`: Delete a comment (only if you are the author).

### Search and Pagination
- Search posts by title or content: `/api/posts/?search=keyword`
- Paginate through posts: `/api/posts/?page=2`

## Follow Management

- **Follow a User**:
  - `POST /api/accounts/follow/<user_id>/`: Follow a specific user by their ID.
  - Example request:
    ```bash
    curl -X POST -H "Authorization: Token <your_token>" http://localhost:8000/api/accounts/follow/2/
    ```

- **Unfollow a User**:
  - `POST /api/accounts/unfollow/<user_id>/`: Unfollow a specific user by their ID.

## User Feed

- **Retrieve Feed**:
  - `GET /api/feed/`: Retrieve a feed of posts from users the authenticated user follows, ordered by creation date (most recent first).
  - Example request:
    ```bash
    curl -X GET -H "Authorization: Token <your_token>" http://localhost:8000/api/feed/
    ```

## Model Changes
- **CustomUser Model**:
  - Added `followers` and `following` fields (many-to-many relationships to handle follow functionality).
