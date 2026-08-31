2. Tech stack
Computer Vision: YOLO Pose (ONNX), ONNX Runtime, OpenCV, ByteTrack, Temporal Fall Classifier, YuNet & SFace.
Backend: FastAPI, WebSocket, Pydantic, LangChain / LangGraph.
Data & Storage: PostgreSQL, Redis, MinIO Object Storage.
Streaming: MediaMTX, WebRTC/HLS, FFmpeg, SSH Reverse Tunnel cho camera LAN.
Frontend: React, TypeScript, Vite, hls.js, Canvas overlay; prototype React Native.
DevOps: Docker Compose, Caddy HTTPS, uv, pnpm, Pytest, Ruff, MyPy.

3. Traction
Production-ready: Web, API và Media Gateway đã triển khai thực tế trên VPS; kết nối thành công camera IP LAN qua SSH Tunnel.
Software Quality: 240/240 automated tests passed, Ruff & TypeScript type-check đạt 100%.
Fall Detection Performance: 83.05% F1, 80.32% precision, and 85.96% recall
Runtime: YOLO26n-pose đạt khoảng 8-15 FPS còn tùy thuộc vào mạng.
Real-time Alerts: Tự động phát hiện té ngã/bất động, gửi email kèm snapshot/video evidence.
