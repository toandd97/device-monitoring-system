1. Mục tiêu									
	Ứng viên xây dựng một hệ thống backend đơn giản theo mô hình microservices.								
	Hệ thống gồm các services nhận dữ liệu, xử lý dữ liệu và bắn cảnh báo khi phát sinh sự cố.								
	Bài test đánh giá khả năng thiết kế API, xử lý bất đồng bộ, message queue, database và triển khai bằng Docker.								
									
2. Bối cảnh									
	Giả sử công ty đang xây dựng một hệ thống giám sát trạng thái từ các device/services (như CPU, RAM, dung lượng ổ đĩa...). 								
	Các thiết bị sẽ gửi dữ liệu theo chu kỳ về hệ thống này, hệ thống sẽ tiếp nhận thông tin trạng thái và phân tích dữ liệu nhận được								
	Nếu hệ thống phát hiện giá trị bất thường thì sẽ gửi cảnh báo tới nhân sự vận hành thông qua chat								
									
3. Yêu cầu ứng dụng có các chức năng									
	- Tiếp nhận các cảnh báo từ thiết bị thông qua RestAPI								
	- Thực hiện phân tích cảnh báo và so sánh với ngưỡng đã đặt ra, lưu lại kết quả 								
	- Sau khi có kết quả so sánh thì sẽ thực hiện gửi thông báo khi cảnh báo critical/error								
									
4. Yêu cầu kỹ thuật									
	- Áp dụng kiến trúc microservice, triển khai >= 2 services								
	- Sử dụng ngôn ngữ lập trình Python								
	- Có sử dụng message queue và background task / long-running task								
	- Sử dụng database PostgresSQL hoặc MongoDB								
	- Sử dụng Docker và DockerCompose để triển khai								
									
5. Bổ sung thêm									
	- Ứng viên chỉ cần xây dựng ứng dụng với các dữ liệu đơn giản 								
	- Ứng viên có thể gửi thông báo thông qua các nền tảng chat như telegram hoặc discord để đơn giản hóa việc coding								
	- Ứng viên có thể sử dụng các công cụ khác hỗ trợ xây dựng ứng dụng								
	- Ứng viên thực hiện code và đẩy lên github 								
									
6. Dữ liệu tham khảo									
	- Cảnh báo 								
		{							
			device_id: "router-01",						
			metric: "cpu_usage",						
			value: 92,						
			timestamp: "2025-12-10T10:00:00Z"						
		}							
									
	- Ngưỡng cpu								
		{							
			normal: 60,						
			warning: 61,						
			critical: 80,						
		}							
									