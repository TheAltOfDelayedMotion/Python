from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth

callsignlaptop1 = "laptop"
callsignlaptop2 = "jaydens_laptop"
callsigniPhone1 = "iphone"
callsigniPhone2 = "phone"
callsigntv1 = "tv"
callsigntv2 = "samsung tv"

actuallaptopname = "JAYDENS_LAPTOP"
actualiPhonename = "iPhone"
actualtvname = "TOBEADDED"

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="80f245f716174488b68c8d33d081a863",
                                               client_secret="6eaa228cb71b4a5dad8353dc3d7e271d",
                                               redirect_uri="http://localhost:1234",
                                               scope=scope,open_browser=True))

spotipy.util.prompt_for_user_token()

def currentlyPlaying(justReturnSongInfo = False):
    data = sp.current_playback(market="US", additional_types=None)
    playbackInfo = ""
    songOnlyPlaybackInfo = ""

    if data != None:
        songdata = data.get("item") #First layer
        currentsong = songdata.get("name") #Second layer information
        songartistsdata = songdata.get("artists") #Third layer information
        #print(songartistsdata)
        songartistsfurtherdata = songartistsdata[0] #Forth layer information
        songartists = songartistsfurtherdata.get("name") #Five layer information
        active_device = getDeviceInfo()
        
        songOnlyPlaybackInfo = f"{currentsong} [{songartists}]"
        playbackInfo = f"Currently playing on {active_device}: {currentsong} [{songartists}]"
        #print(playbackInfo)
        
    else:
        playbackInfo = "Spotify is not currently playing anything..."
        #print("Spotify is not currently playing anything...")
    
    if justReturnSongInfo == True:
        return songOnlyPlaybackInfo
    
    else: 
        return playbackInfo

def getDeviceID(device_name, returnaslist = False):
    deviceID = ""
    data = []
    data = getDeviceInfo(returnalldeviceids=True)
    no_of_active_devices = int(data[0])
    count = 1
    
    device_name = device_name.lower()
    
    if device_name == callsignlaptop1:
        device_name = actuallaptopname
        
    if device_name == callsignlaptop2:
        device_name = actuallaptopname
    
    if device_name == callsigniPhone1:
        device_name = actualiPhonename
        
    if device_name == callsigniPhone2:
        device_name = actualiPhonename
    
    #print(data)
    #print(device_name)
    done = False
    for x in range(no_of_active_devices):
        temp = data[count]
        #print(f"datacount {temp}")
        if temp == device_name:
            count += 1
            deviceID = data[count]
            done = True
            
        elif temp != device_name and done == False:
            count += 3
            #print(temp)
    
    #print(f"DEVICEID {deviceID}")
    if deviceID != "" and returnaslist == False:
        return deviceID
    
    elif deviceID != "" and returnaslist == True:
        #print(f"Device: {device_name} | ID: {deviceID}")
        returndata = [device_name, deviceID]
        return returndata
    
    else:
        #print("Error, Device not found!")
        returndata = ["none", "Device is not active!"]
        return returndata
        
def getDeviceInfo(returnalldeviceids = False):
    spotifydeviceinfo = [0]
    activeDevices = ""
    
    devicesrawdata = sp.devices()
    devicesdata = devicesrawdata.get("devices")
    #print(devicesdata)
    
    for device in devicesdata:
        spotifydeviceinfo[0] += 1 #number of devices
        
        nameofdevice = device.get("name")
        idofdevice = device.get("id")
        isActive = device.get("is_active")

        spotifydeviceinfo.append(nameofdevice)
        spotifydeviceinfo.append(idofdevice)
        spotifydeviceinfo.append(isActive)
        
    #print(spotifydeviceinfo)
    
    if returnalldeviceids:
        #print(spotifydeviceinfo)
        return spotifydeviceinfo
    
    elif returnalldeviceids == False: 
        count = 1
        for x in range(spotifydeviceinfo[0]):
            deviceName = spotifydeviceinfo[count]
            count += 1
            deviceID = spotifydeviceinfo[count]
            count += 1
            isDeviceActive = spotifydeviceinfo[count]
            count += 1
            
            if isDeviceActive == True:
                activeDevices = activeDevices + str(deviceName)
            
        if activeDevices != "":
            #print(activeDevices)
            return activeDevices
        
        else:
            return "No Active Devices on Spotify..."

def pause():
    if (getDeviceInfo() == "No Active Devices on Spotify..."):
        print("No Active Devices on Spotify...")
    
    elif (currentlyPlaying() == "Spotify is not currently playing anything...") and (getDeviceInfo() != "No Active Devices on Spotify..."):
        print("Spotify is not currently playing.")
    
    elif (currentlyPlaying() != "Spotify is not currently playing anything...") and (getDeviceInfo() != "No Active Devices on Spotify..."):
        try:
            sp.pause_playback()
            print("Spotify Playback Paused...") 
            
        except spotipy.exceptions.SpotifyException:
            print("Spotify Playback is already paused...")
    
    else:
        print("HUH??? Spotify module error btw")
    
def play(song = None, song_artist = None, uridata=None):
    if song!= None:
        songdata = searchSpotifySongData(song, song_artist)
        uridata = songdata.get("uri")
    
    uri = [uridata]
    #if song was not found, uridata = None
    
    if (getDeviceInfo() == "No Active Devices on Spotify..."):
        print("No Active Devices on Spotify...")
    
    elif (currentlyPlaying() == "Spotify is not currently playing anything...") and (getDeviceInfo() != "No Active Devices on Spotify..."):
        sp.start_playback(uris=uri)
        print("Spotify Playback Started...")
        print(currentlyPlaying())
        sleep(1)
    
    elif (currentlyPlaying() != "Spotify is not currently playing anything...") and (getDeviceInfo() != "No Active Devices on Spotify..."):
        try:
            sp.start_playback(uris=uri)
            print("Spotify Playback Started...")
            sleep(1)
            print(currentlyPlaying())
            
        except spotipy.exceptions.SpotifyException:
            print("Spotify is already playing!")
            
    else:
        print("broooo something wrong with spotify module")

def switchDevice(device_name, force_play=True):
    device_id = []
    device_id = getDeviceID(device_name, returnaslist=True)
    
    #print(f"device_id[1]{device_id[1]}")
    
    if device_id[1] != "Device is not active!":
        sp.transfer_playback(str(device_id[1]), force_play)
        print(f"Currently playing on {device_id[0]}: {currentlyPlaying(justReturnSongInfo=True)}")
        
    else:
        print(device_id[1])

def searchSpotifySongData(song_name, song_artist=None, numberofresults=1):
    cont = True
    if song_name == "":
        print("No song search query!")
        cont = False
    
    if song_artist == None:
        songquery = song_name
        
    else:
        songquery = f"{song_name}, {song_artist}"
    
    searchResults = []
    returndata = {}
    
    if cont:
        for i in range(numberofresults):
            rawdata = sp.search(songquery, limit=numberofresults, market='SG')
            #print(rawdata)
            tracksraw = rawdata.get("tracks")
            tracksdata = tracksraw.get("items")
            
            try:
                songdata = tracksdata[0] #get first track
                
            except IndexError:
                print(f'Song "{songquery}" was not found!')
                break
            
            songName = songdata.get("name")
            songURI = songdata.get("uri")
            songArtistData = songdata.get("artists")
            songArtistData = songArtistData[0]
            songArtist = songArtistData.get("name")
            songAlbumData = songdata.get("album")
            songAlbum = songAlbumData.get("name")
        
            returndata["name"] = songName
            returndata["uri"] = songURI
            returndata["artist"] = songArtist
            returndata["album"] = songAlbum
            #returndata = [songName, songURI, songArtist, songAlbum]
            searchResults.append(returndata)
                
        if numberofresults == 1:
            return returndata #{'name': "Don't Know Why", 'uri': 'spotify:track:1zNXF2svmdlNxfS5XeNUgr', 'artist': 'Norah Jones', 'album': 'Come Away With Me (Super Deluxe Edition)'}
        
        else:
            return searchResults    
        
    else:
        return {}

def testFeatures():
    print(f"{currentlyPlaying()} \n")
    print(f"{getDeviceInfo()} \n")
    print(f"{getDeviceID('iphone')} \n")
    sleep(2)
    pause()
    sleep(2)
    play()
    sleep(2)
    switchDevice("laptop")
    sleep(5)
    switchDevice("iphone")
    sleep(5)
    switchDevice("laptop")

def addtoQueue(song, song_artist = None):
    songdata = searchSpotifySongData(song, song_artist)
    song_name = songdata.get("name")
    song_artist = songdata.get("artist")
    
    if songdata.get("uri") != None:
        try:
            sp.add_to_queue(songdata.get("uri"))
            print(f'Adding {song_name} [{song_artist}] to the queue!')
            
        except spotipy.exceptions.SpotifyException:
            print("No Active Devices on Spotify...")
            
    else:
        if songdata != {}:
            print(f'Unable to add "{song}" to the queue...')

def skip():
    try:
        sp.next_track()
        print(f"Skipping: {currentlyPlaying(justReturnSongInfo=True)}")
        
        sleep(1)
        print(f"Playing: {currentlyPlaying(justReturnSongInfo=True)}")
        
    except spotipy.exceptions.SpotifyException:
        print("No Active Devices on Spotify...")

def rewind():
    try:
        sp.previous_track()
        sleep(1)
        print(f"Rewinding to: {currentlyPlaying(justReturnSongInfo=True)}")
        
    except spotipy.exceptions.SpotifyException:
        print("No Active Devices on Spotify...")

def getPlaylist():
    data = sp.current_user_playlists(limit=50, offset=0)
    playlists = data.get("items") #items in return
    #print(playlists)
    
    for playlist in playlists:
        print(playlist.get("name"))
        print(playlist.get("id"))

