REFRESH_PAGES = Logout.html addRelay.html changePasswordPost.html changePlaylist.html changeRelay.html changeUserAccess.html changeUserWallPostAccess.html deleteRelay.html deleteRequests.html editUserPost.html holdRequests.html imFeelingPopular.html kill.html login.html randomizeRequests.html releaseRequests.html request.html submitAdmin.html swapRequests.html verify.html wallPost.html
 

links: .refresh-links .userInfo-links
.userInfo-links: userInfo.py userInfo.html
	ln -s userInfo.py statMyInfo.py
	ln -s userInfo.html statMyInfo.html
	touch .userInfo-links

.refresh-links: refresh.html
	for a in $(REFRESH_PAGES); do ln -s refresh.html $$a; done
	touch .refresh-links

clean:
	rm statMyInfo.py statMyInfo.html 2> /dev/null || /bin/true
	for a in $(REFRESH_PAGES); do rm $$a 2> /dev/null ||true; done
	rm .userInfo-links .refresh-links 2> /dev/null || true
