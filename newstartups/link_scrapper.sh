# Activate the virtual environment
source ~/startups/env/bin/activate

# Navigate to the script directory
cd ~/startups/shushant-startups/newstartups


# Create log directory if it doesn't exist
mkdir -p log

# Get timestamp
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Define log file path
log_file="log/link_scraper_run.log"

# Run the scraper
echo "Running crunch_link_scraper1.py..." | tee -a "$log_file"
/home/user1/startups/env/bin/python /home/user1/startups/shushant-startups/newstartups/crunch_link_scraper1.py

# * * * * * /home/user1/startups/shushant-startups/newstartups/detail_scrapper.sh >> /home/user1/startups/shushant-startups/newstartups/log/detail_scrapper.log 2>&1
# * * * * * /home/user1/startups/shushant-startups/newstartups/crunch_link_scraper1.sh >> /home/user1/startups/shushant-startups/newstartups/log/crunch_link_scraper.log 2>&1
