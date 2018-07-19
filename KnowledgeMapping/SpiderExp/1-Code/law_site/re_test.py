text = """
		(function($) {
			$(function() {
				queryProgress("a9463d8b340d466b8b1dc973b7549c60");
			});
			function queryProgress(progressId) {
				$.get( $ctx + "/progressManager.jsp?progressId=" + progressId, function(data) {
					if (!data) {
						$("#progress").text("无任务！");
					} else if (data.finished) {
						var description = "";
						if (data.description) {
							description = data.description;
						}
						if (data.value) {
							description = data.description + "..." + data.value;
						}
						if (data.total) {
							description = description +  " / " + data.total;
						}
						if (description) {
							$("#progress").text(description);
						}
						if (data.value) {
							$("#download-button").show();
						}
						return;
					} else {
						if (data.description && data.value && data.total) {
							$("#progress").text(data.description + "..." + data.value + " / " + data.total);
						}
						setTimeout(function() {
							queryProgress(progressId);
						}, 250);
					}
				});
			}
			$('#download-button').click(function() {
				window.open($ctx + "/service/rest/tk.File/a9463d8b340d466b8b1dc973b7549c60/download");
			});
			
			$('#downlaod-start-pdf').click(function() {
				download("pdfzip");
			});
			
			$('#downlaod-start-xlsx').click(function() {
				download("xlsx");
			});
			
			function download(action) {
				var progressId = "a9463d8b340d466b8b1dc973b7549c60";
				$.ajax({
					type : 'post',
					url : $ctx + '/service/rest/opendata.Judgement/collection/' + action,
					data : '_csrf=891196de-6892-4b95-8ff1-43a091c2ec51&size=' + $("#download-size").val() + '&showResults=true&keyword=%E6%8A%95%E8%B5%84&causeId=&caseNo=&litigationType=&docType=&litigant=&plaintiff=&defendant=&thirdParty=&lawyerId=&lawFirmId=&legals=&courtId=&judgeId=&clerk=&judgeDateYear=&judgeDateBegin=2018-01-01&judgeDateEnd=2018-02-01&zone=%E6%B2%B3%E5%8D%97%E7%9C%81&procedureType=&lawId=&lawSearch=&courtLevel=&judgeResult=&page=2' + '&action=' + action + '&progressId=' + progressId,
					success: function (data) {
						console.log(data);
					}
				});
				location.href = $ctx + "/progress.jsp?progressId=" + progressId;
			}
		})(jQuery);
	"""

import re

progress_csrf_value = re.findall(r"'_csrf=(891196de-6892-4b95-8ff1-43a091c2ec51)&size='", text)[0]
print(progress_csrf_value)


"""
1.
get
请求初始页面选择数量 抽取progress和csrf
http://openlaw.cn/progress.jsp?showResults=true&keyword=%E6%8A%95%E8%B5%84&causeId=&caseNo=&litigationType=&docType=&litigant=&plaintiff=&defendant=&thirdParty=&lawyerId=&lawFirmId=&legals=&courtId=&judgeId=&clerk=&judgeDateYear=&judgeDateBegin=&judgeDateEnd=&zone=%E6%B2%B3%E5%8D%97%E7%9C%81&procedureType=&lawId=&lawSearch=&courtLevel=&judgeResult=
queryProgress("34bf43ff6d524c7a81d02dd51192449d");
window.open($ctx + "/service/rest/tk.File/34bf43ff6d524c7a81d02dd51192449d/download");
var progressId = "34bf43ff6d524c7a81d02dd51192449d";
data : '_csrf=261d9d64-aebf-468e-8dbb-c5c62960bf83&size=' +

get
发送信号
http://openlaw.cn/progressManager.jsp?progressId=34bf43ff6d524c7a81d02dd51192449d
X-NWS-LOG-UUID: 6ee542b4-754f-41ff-a61b-fdc40ef519cc 5c0e51a334e6d32dc3cdcf8c3810d616

http://openlaw.cn/progress.jsp?progressId=34bf43ff6d524c7a81d02dd51192449d
queryProgress("34bf43ff6d524c7a81d02dd51192449d");
data : '_csrf=261d9d64-aebf-468e-8dbb-c5c62960bf83&size=' 

2.
post 发送下载参数
http://openlaw.cn/service/rest/opendata.Judgement/collection/xlsx
_csrf=261d9d64-aebf-468e-8dbb-c5c62960bf83&size=2&showResults=true&keyword=%E6%8A%95%E8%B5%84&causeId=&caseNo=&litigationType=&docType=&litigant=&plaintiff=&defendant=&thirdParty=&lawyerId=&lawFirmId=&legals=&courtId=&judgeId=&clerk=&judgeDateYear=&judgeDateBegin=&judgeDateEnd=&zone=%E6%B2%B3%E5%8D%97%E7%9C%81&procedureType=&lawId=&lawSearch=&courtLevel=&judgeResult=&action=xlsx&progressId=34bf43ff6d524c7a81d02dd51192449d
{"code":1,"javaClass":"com.homolo.framework.service.ServiceResult","structSupport":true,"description":"下载任务已完成！"}

get 返回页面
http://openlaw.cn/progress.jsp?progressId=34bf43ff6d524c7a81d02dd51192449d  页面


get 导出信号 导出id
http://openlaw.cn/progressManager.jsp?progressId=34bf43ff6d524c7a81d02dd51192449d
{"total":2,"dateStart":"2018-07-19T15:33:37+08:00","javaClass":"com.homolo.framework.util.Progress","description":"正在导出至表[Sheet0]","finished":true,"id":"34bf43ff6d524c7a81d02dd51192449d","dateEnd":"2018-07-19T15:33:38+08:00","value":2}

3. 
get  下载
http://openlaw.cn/service/rest/tk.File/34bf43ff6d524c7a81d02dd51192449d/download


"""