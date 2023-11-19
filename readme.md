## Suika Blog System
backend purely driven by fastapi, frontend by vue. 

### Security

OAuth2 + JWT

### Cache
Redis + Beaker 


### Database
```mermaid
graph TD

subgraph Blog
  blog_name
  blog_description
  admin_name
  admin_username
  admin_email
  admin_avatar
  admin_hashed_password
  create_time
  version
end

subgraph Visitor
  id
  user_name
  email
  url
  is_banned
  hashed_info
  create_time
  last_active_time
end

subgraph Article
  id
  title
  content
  word_count
  cover_url
  description
end

subgraph Media
  id
  name
  size
  is_local
  remote_url
  owner_id
  create_time
end

subgraph Tag
  id
  name
end

subgraph Comment
  id
  create_time
  content
  owner_id
  by_admin
  author_id
end

Blog -->|1| Article
Visitor -->|1-n| Comment
Article -->|1-n| Comment
Article -->|1-n| Media
Article -->|m-n| Tag
Tag -->|m-n| Article
```
### run
you may installing the environment and run this project via `make`, or use direct `uvicorn` to run `main:app`


under developing...
