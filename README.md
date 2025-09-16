# Genrify
Sorts saved playlists and albums from Spotify.
Original idea and repo from: https://github.com/mattbrock/genrify

Start Frontend:
Change to frontend folder
Dev: npm run dev
Prod: npm run start

Start Backend:
Change to backend folder
pip install -r requirements.txt
python3 app.py

Start Redis server:
redis-server --port 6376

Build images:
cd backend
docker build -t genrify-backend .
cd ../frontend
docker build -t genrify-frontend .
cd ..

Start Docker stack(Need to create swarm, add secrets, and create network):
Docker stack deploy --compose-file docker-compose.yaml genrify
