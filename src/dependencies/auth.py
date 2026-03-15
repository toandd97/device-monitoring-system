"""
Auth Dependencies — Skeleton cho việc phân quyền per-route.
"""

# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#
# security = HTTPBearer()
#
#
# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ) -> dict:
#     """
#     Verify JWT token và trả về thông tin user.
#     Middleware đã attach token, dependency này decode và validate.
#
#     Returns:
#         dict: {"user_id": "...", "role": "admin" | "viewer" | "device"}
#
#     Raises:
#         HTTPException 401: Token không hợp lệ hoặc hết hạn.
#     """
#     token = credentials.credentials
#     user = _verify_jwt(token)   # TODO: implement JWT decode
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# def require_role(*roles: str):
#     """
#     Dependency factory — kiểm tra role của user hiện tại.
#
#     Args:
#         *roles: Danh sách roles được phép truy cập route này.
#
#     Usage:
#         dependencies=[Depends(require_role("admin", "device"))]
#
#     Raises:
#         HTTPException 403: User không có quyền.
#     """
#     def _check(user: dict = Depends(get_current_user)):
#         if user.get("role") not in roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Access denied. Required: {roles}, got: '{user.get('role')}'",
#             )
#         return user
#     return _check
#
#
# def _verify_jwt(token: str) -> dict | None:
#     """TODO: Decode và verify JWT token."""
#     # import jwt
#     # try:
#     #     payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
#     #     return payload
#     # except jwt.ExpiredSignatureError:
#     #     return None
#     # except jwt.InvalidTokenError:
#     #     return None
#     pass
