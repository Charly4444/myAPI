from database import engine, SessionLocal, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models
from routers import post, user, auth, vote


from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)    # This creates all our models while we're still testing in DEV

app = FastAPI()

# The CORSMiddleware will execute first when our API receives a request
# before the access to our database can be granted, We set it up as follows:

# origins = ["https://www.google.com"]  # We could do this on same line below if list isn't too long or when specifying *
origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,       # we're allowing specified domains as above
                   allow_credentials=True,
                   allow_methods=["*"],         # we're allowing all requests
                   allow_headers=["*"],         # we're allowing all headers
                   )

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
# we just split our path operations to other folders for ease
# the statements above make sure that when we receive a path operation it forwards to all routers
# and matches it with the right one

