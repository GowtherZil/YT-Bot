
import youtube_dl

from youtubesearchpython import VideosSearch

from telegram.ext import Updater , CommandHandler , MessageHandler , Filters , CallbackQueryHandler , InlineQueryHandler 

from random import getrandbits
import time , datetime , os 


from telegram import InlineKeyboardButton , InlineKeyboardMarkup , InlineQueryResultArticle,InputTextMessageContent


ID_2 = int(os.environ["YOUR_ID"])

YOUR_ID = int(os.environ["ID_2"])

TOKEN = os.environ["TOKEN"]

def  alert (Update , context):
	
	
	Update.message.reply_text("🔒Este bot es de uso privado de @Yanco148, si desea tener permiso a el debe hablar con el desarrollador ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="💠Desarrollador💠" , url="https://t.me/Yanco_Dev")]]))	



def start(Update , context) :
    
    user_id=Update.effective_user.id
    
    name=Update.effective_user.first_name
    
    if user_id==YOUR_ID:		
        
        b1 = InlineKeyboardButton(text="🔍Buscar Videos",switch_inline_query_current_chat="")
        
        Update.message.reply_text(f"👋Hey {name} Bienvenido",reply_markup=InlineKeyboardMarkup ([[b1]]))
    	
    else :
    	alert(Update,context)
	
	
# segundo usuario	
def start(Update , context) :
    
    user_id=Update.effective_user.id
    
    name=Update.effective_user.first_name
    
    if user_id==ID_2:
        
        b1 = InlineKeyboardButton(text="🔍Buscar Videos",switch_inline_query_current_chat="")
        
        Update.message.reply_text(f"👋Hey {name} Bienvenido",reply_markup=InlineKeyboardMarkup ([[b1]]))
    	
    else :
    	alert(Update,context)	
    







def messagehandler (Update,context):
    
    
    try:
    	user_id = Update.effective_user.id
    	
    	if user_id == YOUR_ID:
    		url = Update.message.text
    		message= Update.message.reply_text("Obteniendo información.🔹")
    		message_id = message.message_id
    		
    		if "https://www.youtube.com/watch?v=" in url or "http://www.youtube.com/watch?v=" in url:


    			ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    			
    			with ydl:
    			 
    			 result = ydl.extract_info(url,download=False)
    			
    			if 'entries' in result:
    				video = result['entries'][0]
    			else:
    				video = result
    				
    			context.bot.edit_message_text(chat_id=YOUR_ID,message_id=message_id ,text="Obteniendo información.🔹🔹")    			
    			
    			
    			title = video["title"]
    			    			
    			description = video["description"]
    			
    			thumb = video["thumbnail"]
    			
    			duration = video["duration"]
    			
    			duration= datetime.timedelta(seconds=duration)
    			
    			views = video["view_count"]
    			
    			formats = video["formats"]
    			
    			video_id = video["id"]
    			
    			list_formats = []
    			
    			for i in formats:
    				size = i["filesize"]
    				try :
	    				tam=size/1024/1024
	    				tam= str(round(tam,2)) + "MG"
	    				
	    				resolution = i["format_note"]
	    				format_id = i["format_id"]
	    				
	    				list_formats.append([tam,resolution,format_id])
    				except : pass
    				
    			BTN = []
    			for i in list_formats:
    				size = i[0]
    				format = i[1]
    				format_id=i[2]
    				
    				
    				boton= InlineKeyboardButton(text=f"{size} - {format}" , callback_data=f"{format_id}={video_id}")
    				BTN.append(boton)
    				
    			BTNF = []
    			n=0
    			
    			for i in BTN:
    				if n % 2 == 0:
    					
    					try:
    						BTNF.append([BTN[n],BTN[n+1]])
    					except :
    						BTNF.append([BTN[n]])
    				n += 1
    				
    				
    				    			
    			
    			
    			
    			
    			
    			context.bot.edit_message_text(chat_id=YOUR_ID,message_id=message_id ,text="Hecho✅")     			
    			
    			Update.message.reply_text(text=f'<b><a href="{thumb}">📹</a>{title}</b>\n\n{description}\n\n⏳{duration}  👁‍🗨{views}' , parse_mode="html",reply_markup=InlineKeyboardMarkup(BTNF))					
    		 		
    		
    		else :
    			context.bot.edit_message_text(chat_id=YOUR_ID,message_id=message_id ,text="Url inválido.❌")
    			    		
    	else :
    		alert(Update,context)
    		    		
    except AttributeError as error :
    	print(error)

def callbackhandler (Update,context):
	
	query=Update.callback_query
	
	callback_id = Update.callback_query.id
	
	context.bot.answer_callback_query(callback_query_id = callback_id , text = "📦 Descargando..."  , show_alert=False)
	
	data = query.data
	
	#Format
	
	format = data[:data.find("=")]
	
	#Link
	
	video_id = data[data.find("=")+1:]
	
	video_url="https://www.youtube.com/watch?v=" + video_id
	
	#Video title
	
	title = Update.callback_query.message.text[1:Update.callback_query.message.text.find("\n\n")]

	ydl_opts = {'format':format , "outtmpl": "Videos/%(title)s.%(ext)s"}
	
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		
		
		ydl.download([video_url])
	
	context.bot.send_chat_action(chat_id=Update.effective_user.id, action = "UPLOAD_DOCUMENT" )
	
	v = os.listdir("Videos/")
	filename = v[0]
	if filename == ":).txt":
		filename = v[1]
	

	
	Update.callback_query.message.reply_document(document=open("Videos/" + filename,"rb") , filename=filename ,caption=title,reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton(text="🔍Buscar Videos",switch_inline_query_current_chat="")]]))
	
	os.remove(f"Videos/{filename}")


def searchinline (Update,context):
	
	try :
	
		query_id=Update.inline_query.id
		query=Update.inline_query.query
		
		user_id = Update.effective_user.id
		
		if user_id == YOUR_ID :
				
			
			results=[]
			
			search = VideosSearch(query,limit=10)
			
			resultsearch = search.result()
			
			for video in resultsearch["result"]:
				
				title=video["title"]
				
				duration = video["duration"]
				
				viewcount = video["viewCount"]["short"]
				
				thumbnails = video["thumbnails"][0]["url"]
				
				url = video["link"]
				
				results.append(InlineQueryResultArticle(id=hex(getrandbits(64))[2:],title=title,  input_message_content=InputTextMessageContent(url),description=f"{duration}  {viewcount}", thumb_url=thumbnails))
			
			context.bot.answer_inline_query(query_id,results , is_personal=True , cache_time=1)
		
	
	
		else :
			

				
			results=[]
			
			consulta = InlineQueryResultArticle(id=hex(getrandbits(64))[2:],title="🔒",  input_message_content=InputTextMessageContent("🔒"),description=f"Este bot es de uso privado")
			
			results.append(consulta)
			
			context.bot.answer_inline_query(query_id,results,is_personal=True)	
	
	
	except Exception as error :
		time.sleep(5)
		searchinline(Update,context)
		


if __name__ == '__main__':

	updater = Updater(token=TOKEN)
	
	update = Updater
	dp = updater.dispatcher
	
	dp.add_handler(CommandHandler("start",start))
	
	dp.add_handler(MessageHandler(Filters.text,messagehandler))
	
	dp.add_handler(CallbackQueryHandler(pattern=0,callback=callbackhandler))
	
	dp.add_handler (InlineQueryHandler (searchinline))

		
	updater.start_polling()
	print("Run...")
	updater.idle()
