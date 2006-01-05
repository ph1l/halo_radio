
REFRESH_PAGES = verify.html deleteUserPost.html deleteRequests.html editUserPost.html randomizeRequests.html request.html swapRequests.html login.html Logout.html changePasswordPost.html changePlaylist.html enableUserPost.html disableUserPost.html kill.html wallPost.html zipRequests.html holdRequests.html releaseRequests.html addRelay.html deleteRelay.html changeRelay.html

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
