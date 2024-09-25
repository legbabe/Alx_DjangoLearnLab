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

