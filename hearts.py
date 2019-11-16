from bs4 import BeautifulSoup


## Heart Count Plugin
#
class HeartCount():
  ##############################################################################
  # Plugin Settings
  ##############################################################################
  
  # Define the parent ZSM object so we can call its functions and access its 
  # data. Set this in load_config
  z_obj = None
  
  # Settings dict
  settings = {}
  settings['run_id'] = 'current'
  settings['selectors'] = ['h1','h2']

  # Local data dict
  data = {}

  ##############################################################################
  # Helper Functions
  ##############################################################################
  def get_text(self, url_id, doc):
    date_time = 0
    rlys = 0
    rts = 0
    likes = 0
    parse = BeautifulSoup(doc, 'html.parser')
    # print('hello')
    # for selector in self.settings['selectors']:
      # print(selector)  
      # item = parse.find_next(selector)
      # print(item)
    # action_count = parse.find_next('span',{'class':'ProfileTweet-actionCount'})
    # action_count = parse.find_next('span')
    # action_count = parse.a.find_next('.div')
    # action_count = parse.find_next('div')
    # print(action_count.descendants)
    
    #for part in parse.select('.content'):
    #    print(part)

    
    self.z_obj.pprint(len(parse.select('.ProfileTweet-actionList.js-actions')))
    i=0
    for item in parse.select('.ProfileTweet-actionList.js-actions'):
      i+=1
      self.z_obj.pprint(i,0)
      rlys = 0
      rts = 0
      likes = 0
      for action_item in item.children:
        # print(action_item.name)
        self.z_obj.pprint(action_item)
        # if action_item == None:
          # print(' N')
        # if action_item != None:
        if action_item.name == 'div':
          # if 'class' in action_item.attrs: 
          if action_item.get('class') != None: 
            # print('hey!class')
            # print(action_item.attrs)
            if 'ProfileTweet-action--reply' in action_item.attrs['class']:
              # print('0 rly')
              ac = action_item.select('.ProfileTweet-actionCount')[0]
              # print('ac',ac)
              if 'data-tweet-stat-count' not in ac:
                  continue
              rlys = ac.attrs['data-tweet-stat-count']
              # print('rlys:', rlys)
            if 'ProfileTweet-action--retweet' in action_item.attrs['class']:
              # print('1 rt')
              if 'data-tweet-stat-count' not in ac:
                  continue
              rts = action_item.select('.ProfileTweet-actionCount')[0].attrs['data-tweet-stat-count']

              # print(rts)
            if 'ProfileTweet-action--favorite' in action_item.attrs['class']:
              # print('2 fav')
              if 'data-tweet-stat-count' not in ac:
                  continue
              likes = action_item.select('.ProfileTweet-actionCount')[0].attrs['data-tweet-stat-count']
              # print(likes)
              actionCounts = [rlys, rts, likes]
              self.z_obj.pprint(actionCounts)
              #
              footer = item.find_parent('div')
              tweet = footer.find_parent('div')
              self.z_obj.pprint(tweet.attrs)
              header = tweet.select('.stream-item-header')
              self.z_obj.pprint(header)
              #print(header.attrs)
              time = header.select('.time')
              self.z_boj.pprint(time)
              # print(time.attrs)
              #timestamp = time.select('.tweet-timestamp')
              #print(_timestamp)
              #_timestamp = timestamp.select('._timestamp')
              #data_time = _timestamp.attrs['data-time']
              #print(data_time)





    # for selector in self.settings['selectors']:
    #   for item in parse.select(selector):
    #     print(item.attrs)
    #     print(selector)
    #     if ('data-time' in item):
    #       #print('datetime test.')
    #       date_time=str(repr(item['data-time']))
    #       print(item['data-time'])
    #     else:
    #       #for s in item.stripped_strings:
    #         #st = str(repr(s))
    #         #self.z_obj.ex('INSERT INTO heart_count VALUES (?,?,?,?,?,?)', (self.z_obj.run_id, url_id, selector, comments, retweets,likes))
    #         #self.z_obj.pprint((self.z_obj.run_id, url_id, selector, st, datatime))
    #         #if selector = likes then insert into database
    #         #if selector = retweet then get
    #       if selector.strip() == 'button.ProfileTweet-actionButton.js-actionButton.js-actionReply .ProfileTweet-actionCount':
    #         #print ('reply.')  
    #         if 'data-tweet-stat-count' in item.attrs:
    #           print('replys',item['data-tweet-stat-count'])
    #       if selector.strip() == 'button.ProfileTweet-actionButton.js-actionButton.js-actionRetweet .ProfileTweet-actionCount':
    #         if 'data-tweet-stat-count' in item.attrs:
    #           print('retweets',item['data-tweet-stat-count'])
    #       if selector.strip() == 'button.ProfileTweet-actionButton.js-actionButton.js-actionFavorite .ProfileTweet-actionCount':
    #         if 'data-tweet-stat-count' in item.attrs:
    #           print('retweets',item['data-tweet-stat-count'])
    #       print([s for s in item.stripped_strings])
    #      # print('test')


  ###########
  # Common data functions



  ##############################################################################
  # Zeomine plugins
  ##############################################################################

  ## Add configs to this module from parent object
  #
  def load_config(self):
    # If we have settings, load them.
    if self.__class__.__name__ in self.z_obj.conf['plugins'] and self.z_obj.conf['plugins'][self.__class__.__name__]:
      conf = self.z_obj.conf['plugins'][self.__class__.__name__]['settings']
      for section in conf:
        if isinstance(conf[section], dict):
          for subsection in conf[section]:
            if section in self.settings:
              self.settings[section][subsection] = conf[section][subsection]
        # If not a dict, assume the section is a single property to set.
        else:
          self.settings[section] = conf[section]
    # Run additonal actions specific to your plugin
    self.z_obj.pprint("Successfully loaded HeartCount.", 0)

  ## Initiate Plugin
  #
  # 
  def initiate(self):
    # Create the data table if it doesn't exist yet
    self.z_obj.excom('CREATE TABLE IF NOT EXISTS heart_count (zeomine_instance text, url int, selector text, comments_text, retweets_text, likes_text)')
    if self.settings['run_id'] == 'current':
      self.settings['run_id'] = self.z_obj.run_id

  ## Evaluate Data
  #
  # 
  def evaluate_data(self):
    doclist = self.z_obj.fetchall('select url,response_text,type from crawler_req_text inner join crawler_basic_data on crawler_req_text.crawl_data=crawler_basic_data.rowid where crawler_req_text.zeomine_instance=?',(str(self.z_obj.run_id),))
    for doc_data in doclist:
      if doc_data[2] == 'internal':
        self.get_text(doc_data[0],doc_data[1])
    #Save the data aftter we are done extracting
    self.z_obj.com()
    pass

  # Authenticate with remote services
  #
  #
  def authenticate(self):
    pass

  ## Send Alerts
  #
  # 
  def alert(self):
    pass

  ## Generate Reports and save data
  #
  # 
  def report(self):
    
    pass

  ## Final actions for Zeomine shutdown
  #
  # 
  def shutdown(self):
    pass

  ##############################################################################
  # Core Crawler - Selenium plugins
  ##############################################################################

  ## Core Selenium Crawler callback
  #
  # 
  def core_crawler_selenium(self, current_url):
    pass
