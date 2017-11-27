window.onload = function(){
	var list = document.getElementById('list');
	var lis = list.children;//children attribute
	var timer;

	//delet node function
	function removeNode(node){
		node.parentNode.removeChild(node);//通过元素的父节点调用 call removeChild from this element's parents' node,and then delete itself
	}
	//likes and share
	function praiseBox(box,el){
		//box for share
		var praiseElement = box.getElementsByClassName('praises-total')[0];//find the element through class
		var oldTotal = parseInt(praiseElement.getAttribute('total')); // get the the value of total
		var txt = el.innerHTML;
		var newTotal;//calculate the new total number
		if(txt =='like'){
			newTotal = oldTotal + 1;
			/*更新框里面的文字update*/
			praiseElement.innerHTML= (newTotal == 1) ? 'I like it':'I and'+ oldTotal +'people like it';
			el.innerHTML = 'cancel like';
		}else{ /* 取消点赞 */
			newTotal = oldTotal - 1;
			/*更新框里面的文字*/
			praiseElement.innerHTML= (newTotal == 0) ? '' : newTotal +'people like it';
			el.innerHTML = 'like';
		}
		praiseElement.setAttribute('total', newTotal);
		praiseElement.style.display = (newTotal == 0) ? 'none' : 'block';
	}
	//发表评论
	function replayBox(box){
		var textarea = box.getElementsByTagName('textarea')[0];
		var list = box.getElementsByClassName('comment-list')[0];
		var li = document.createElement('div');
		li.className = 'comment-box clearfix';
		li.setAttribute('user', 'self');
		var html = '<img class="myhead" src="images/my.jpg" alt="">'+
                        '<div class="comment-content">'+
                            '<p class="comment-text"><span class="user">Me：</span>'+textarea.value+'</p>'+
                            '<p class="comment-time">'+
                                getTime()+
                                '<a href="javascript:;" class="comment-praise" total="0" my="0" style="">Like</a>'+
                                '<a href="javascript:;" class="comment-operate">Delete</a>'+
                            '</p>'+
                        '</div>';
        li.innerHTML= html;
        list.appendChild(li);
        textarea.value = '';
        textarea.onblur();
	}
	/*get dates*/
	function getTime(){
		var t = new Date();
		var y = t.getFullYear();
		var m = t.getMonth()+1;
		var d = t.getDate();
		var h = t.getHours();
		var mi = t.getMinutes();
		m = m < 10 ? '0' + m : m;
		d = d < 10 ? '0' + d : d;
		h = h < 10 ? '0' + h : h;
		mi = mi < 10 ? '0' + mi : mi;
		return y + '-' + m + '-' + d + ' ' + h + ':' + mi;
	}
	/*reply like*/
	function praiseReply(el){
		var oldTotal = parseInt(el.getAttribute('total'));
		var my = parseInt(el.getAttribute('my'));
		var newTotal;
		if(my == 0 ){
			newTotal = oldTotal +1;
			el.setAttribute("total", newTotal);
			el.setAttribute('my', 1);
			el.innerHTML = newTotal+' cancel like';
		}else{
			newTotal = oldTotal -1;
			el.setAttribute("total", newTotal);
			el.setAttribute('my', 0);
			el.innerHTML = (newTotal==0) ? 'like': newTotal+' like';
		}
		el.style.display = (newTotal==0) ? '' : 'inline-block' ;
	}
	/*operateReply*/
	function operateReply(el){
		var commentBox = el.parentNode.parentNode.parentNode;//commentBox
		var box = commentBox.parentNode.parentNode.parentNode;//shareBox
		var textarea = box.getElementsByTagName('textarea')[0];
		var user = commentBox.getElementsByClassName("user")[0];//users' nodes
		var txt = el.innerHTML;
		if(txt=='reply'){
			textarea.onfocus();
			textarea.value = 'reply'+user.innerHTML;
			textarea.onkeyup();
		}else{
			removeNode(commentBox);
		}
	}
	for(var i = 0 ;i<lis.length;i++){
		lis[i].onclick= function(e){
			e = e || window.event;//compatable with ie
			var el = e.srcElement;//存放触发元素
			switch(el.className){
				case 'close':// 获取到 关闭的 a标签
					removeNode(el.parentNode);
					break;
				//like and share
				case 'praise':
					praiseBox(el.parentNode.parentNode.parentNode,el);
					break;
				//reply button turn into grey
				case 'btn btn-off':
					clearTimeout(timer);
					break;
				//reply button blue
				case 'btn':
					replayBox(el.parentNode.parentNode.parentNode);
					break;
				//like,comment
				case 'comment-praise':
					praiseReply(el);
					break;
				//operateReply
				case 'comment-operate':
					operateReply(el);
					break;
			}
		}
		/*input form*/
		var textarea = lis[i].getElementsByTagName("textarea")[0];
		textarea.onfocus = function(){
			this.parentNode.className = 'text-box text-box-on';
			this.value = this.value=='Comment…' ? '' : this.value;
			this.onkeyup();
		}
		textarea.onblur =function(){
			var me = this;//store input variable
			if(this.value==''){
				timer =setTimeout(function(){
					me.parentNode.className = 'text-box';
					me.value ='Comment…' ;
				}, 300);
			}
		}
		//function:calculate words
		textarea.onkeyup = function(){
			var len = this.value.length;
			var p = this.parentNode;
			var btn = p.children[1];
			var word = p.children[2].children[0];
			if(len == 0||len>140){
				btn.className = 'btn btn-off';
			}else{
				btn.className = 'btn';
			}
			word.innerHTML = len;
		}
	}
}
