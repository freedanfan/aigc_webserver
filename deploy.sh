#!/bin/bash

# AIGC Webserver 部署脚本
# 使用方法: ./deploy.sh [环境]
# 环境参数: prod (默认), test

# 设置错误时退出
set -e

# 默认环境为生产环境
ENV=${1:-prod}
echo "开始部署 AIGC Webserver 前端应用 (环境: $ENV)"

# 安装依赖
echo "正在安装依赖..."
npm install

# 根据环境参数选择构建命令
if [ "$ENV" = "test" ]; then
  echo "正在构建测试环境版本..."
  npm run build:test
else
  echo "正在构建生产环境版本..."
  npm run build
fi

# 检查构建结果
if [ ! -d "dist" ]; then
  echo "构建失败，dist 目录不存在!"
  exit 1
fi

echo "构建成功!"

# 创建部署目录
DEPLOY_DIR="deploy_$(date +%Y%m%d_%H%M%S)"
mkdir -p $DEPLOY_DIR

# 复制构建结果和配置文件
echo "正在准备部署文件..."
cp -r dist/* $DEPLOY_DIR/
cp nginx.conf $DEPLOY_DIR/

echo "部署文件已准备完成，位于: $DEPLOY_DIR/"
echo "请将此目录上传到服务器，并按照以下步骤完成部署:"
echo ""
echo "1. 将 $DEPLOY_DIR 目录中的文件上传到服务器的 /usr/share/nginx/html/ 目录"
echo "2. 将 nginx.conf 文件上传到服务器的 /etc/nginx/ 目录"
echo "3. 重启 Nginx: sudo systemctl restart nginx"
echo ""
echo "如果您使用 Docker 部署，请参考 README.md 中的 Docker 部署说明"
echo ""
echo "部署准备完成!" 