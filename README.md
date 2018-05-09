Welcome to WikiVis 
    - a visualization tool for wikipedia article connectivity.

Getting Started:
    At this time, our website is hosted remotely and is blocked from
    interfacing with our server on Tufts campus, therefore it is necessary
    to run the website remotely.

    To run, ensure you have the necessary dependencies by running:
     >> pip install -r requirements.txt
    
    Now, you should be set to spin up the server with python3:
     >> python3 flaskserver.py

    This should host a local server running on http://localhost:5000

    Now follow that link and you should see our website!

Using the Vis:
    Our visualization is slightly performance heavy, but fun and fun-omenally
    interesting. Start typing a wikipedia article name into our search bar
    and select one of the drop down items to ensure you're spelling it
    correctly.
    
    The loading gif will indicate to you that your visualization is loading,
    so please be patient as it can take a while.  The nodes that appear are
    the other articles most connected to that article.  The links represent
    hyperlinks between articles and are shaded according to how many times
    users have clicked between those two articles.  They currently do not show
    the to/from because we wanted to cluster according to connectivity and that
    can look much messier with arrows on the links.  By right clicking on a
    node you can also load that nodes most connected articles into the vis.

    Finally regard the side bar on your right.  On the top, there's an article
    list that shows all the titles of the nodes.  Hovering over nodes or
    titles will cause you to autoscroll to the title and highlight the node and
    title's color.  Clicking on the node or title will allow you to view a
    preview of the related wikipedia page with a link to open it.

Current bugs/next steps:
    Right clicking an article now only displays that article's top links.
    Can only look at one preview at a time
    Nodes stay within bounding box but edges do not
    Occasionally edges point to nodes that aren't there
    No way to see to/from data, nor how many clicks in clickstream
    No link in preview to the wikipedia page


Get in touch!
    Thanks for your interest in our visualization, if you have any comments,
    questions, contributions, etc, definitely let me know!
    daniel.dinjian@gmail.com