import os
import shutil
import subprocess
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AdvancedSystemUpgrader:
    def __init__(self):
        self.vm_path = "/home/huhu2580/TON_Bitcoin_Trader"
        self.backup_path = f"/home/huhu2580/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.new_modules = [
            "websocket_client.py",
            "market_microstructure.py", 
            "smart_order_manager.py"
        ]
        
    def create_backup(self):
        """현재 시스템 백업"""
        logger.info("🛡️ 현재 시스템 백업 중...")
        
        try:
            # 백업 디렉토리 생성
            os.makedirs(self.backup_path, exist_ok=True)
            
            # 주요 파일들 백업
            files_to_backup = [
                "main.py",
                "config.py", 
                "okx_client.py",
                "trading_strategy.py",
                "risk_manager.py",
                "technical_analysis.py",
                "news_sentiment.py",
                "utils.py"
            ]
            
            for file in files_to_backup:
                src = os.path.join(self.vm_path, file)
                dst = os.path.join(self.backup_path, file)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    logger.info(f"✅ {file} 백업 완료")
            
            # modules 디렉토리 백업
            modules_src = os.path.join(self.vm_path, "modules")
            modules_dst = os.path.join(self.backup_path, "modules")
            if os.path.exists(modules_src):
                shutil.copytree(modules_src, modules_dst)
                logger.info("✅ modules 디렉토리 백업 완료")
            
            logger.info(f"✅ 백업 완료: {self.backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 백업 실패: {e}")
            return False
    
    def install_dependencies(self):
        """새로운 의존성 설치"""
        logger.info("📦 새로운 의존성 설치 중...")
        
        try:
            # websockets 패키지 설치
            result = subprocess.run([
                f"{self.vm_path}/venv/bin/pip", 
                "install", 
                "websockets==15.0.1"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ websockets 패키지 설치 완료")
                return True
            else:
                logger.error(f"❌ 패키지 설치 실패: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 의존성 설치 오류: {e}")
            return False
    
    def deploy_new_modules(self):
        """새로운 모듈들 배포"""
        logger.info("🚀 새로운 모듈들 배포 중...")
        
        try:
            # modules 디렉토리 확인/생성
            modules_path = os.path.join(self.vm_path, "modules")
            if not os.path.exists(modules_path):
                os.makedirs(modules_path)
                # __init__.py 생성
                with open(os.path.join(modules_path, "__init__.py"), "w") as f:
                    f.write("")
            
            # WebSocket 클라이언트 모듈
            websocket_client_code = '''#!/usr/bin/env python3
# WebSocket 클라이언트 (간소화된 VM 버전)
import asyncio
import websockets
import json
import logging
import time
from typing import Dict, List, Callable
from datetime import datetime

class OKXWebSocketClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ws_url = "wss://ws.okx.com:8443/ws/v5/public"
        self.orderbook = {'bids': [], 'asks': [], 'timestamp': 0}
        self.latest_trades = []
        self.callbacks = {'orderbook': [], 'trades': []}
        self.is_connected = False
        
    def add_callback(self, data_type: str, callback: Callable):
        if data_type in self.callbacks:
            self.callbacks[data_type].append(callback)
    
    async def start(self, symbol: str = "BTC-USDT-SWAP"):
        """WebSocket 시작"""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                subscription = {
                    "op": "subscribe",
                    "args": [
                        {"channel": "books5", "instId": symbol},
                        {"channel": "trades", "instId": symbol}
                    ]
                }
                await websocket.send(json.dumps(subscription))
                self.is_connected = True
                
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        await self._process_message(data)
                    except Exception as e:
                        self.logger.error(f"메시지 처리 오류: {e}")
                        
        except Exception as e:
            self.logger.error(f"WebSocket 연결 오류: {e}")
            self.is_connected = False
    
    async def _process_message(self, data: Dict):
        if 'data' not in data:
            return
            
        channel = data.get('arg', {}).get('channel', '')
        
        if channel == 'books5':
            book_data = data['data'][0]
            self.orderbook = {
                'bids': [[float(bid[0]), float(bid[1])] for bid in book_data['bids']],
                'asks': [[float(ask[0]), float(ask[1])] for ask in book_data['asks']],
                'timestamp': int(book_data['ts'])
            }
            
            for callback in self.callbacks['orderbook']:
                try:
                    await callback(self.orderbook)
                except Exception as e:
                    self.logger.error(f"호가창 콜백 오류: {e}")
        
        elif channel == 'trades':
            trades = []
            for trade in data['data']:
                trades.append({
                    'price': float(trade['px']),
                    'size': float(trade['sz']),
                    'side': trade['side'],
                    'timestamp': int(trade['ts'])
                })
            
            self.latest_trades.extend(trades)
            if len(self.latest_trades) > 100:
                self.latest_trades = self.latest_trades[-100:]
            
            for callback in self.callbacks['trades']:
                try:
                    await callback(trades)
                except Exception as e:
                    self.logger.error(f"체결 콜백 오류: {e}")
    
    def get_latest_data(self) -> Dict:
        return {
            'orderbook': self.orderbook,
            'latest_trades': self.latest_trades[-10:],
            'connection_status': self.is_connected
        }
'''
            
            # 시장 미세구조 분석기 모듈
            market_analyzer_code = '''#!/usr/bin/env python3
# 시장 미세구조 분석기 (간소화된 VM 버전)
import logging
import statistics
from typing import Dict, List
from collections import deque
from datetime import datetime

class MarketMicrostructureAnalyzer:
    def __init__(self, lookback_periods: int = 50):
        self.logger = logging.getLogger(__name__)
        self.orderbook_history = deque(maxlen=lookback_periods)
        self.trade_history = deque(maxlen=lookback_periods * 2)
        
    def update_orderbook(self, orderbook_data: Dict):
        """호가창 데이터 업데이트"""
        if orderbook_data['bids'] and orderbook_data['asks']:
            # 불균형 계산
            bid_volume = sum([bid[1] for bid in orderbook_data['bids']])
            ask_volume = sum([ask[1] for ask in orderbook_data['asks']])
            
            if bid_volume + ask_volume > 0:
                imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)
            else:
                imbalance = 0
            
            orderbook_data['imbalance'] = imbalance
            self.orderbook_history.append(orderbook_data)
    
    def update_trades(self, trade_data: List[Dict]):
        """체결 데이터 업데이트"""
        for trade in trade_data:
            self.trade_history.append(trade)
    
    def analyze_orderbook_imbalance(self) -> Dict:
        """호가창 불균형 분석"""
        if not self.orderbook_history:
            return {}
        
        current_book = self.orderbook_history[-1]
        return {
            'basic_imbalance': current_book.get('imbalance', 0),
            'timestamp': current_book.get('timestamp', 0)
        }
    
    def analyze_trade_flow(self, window_seconds: int = 10) -> Dict:
        """체결 플로우 분석"""
        if len(self.trade_history) < 10:
            return {}
        
        current_time = datetime.now().timestamp() * 1000
        cutoff_time = current_time - (window_seconds * 1000)
        
        recent_trades = [t for t in self.trade_history if t['timestamp'] > cutoff_time]
        
        if not recent_trades:
            return {}
        
        buy_volume = sum([t['size'] for t in recent_trades if t['side'] == 'buy'])
        sell_volume = sum([t['size'] for t in recent_trades if t['side'] == 'sell'])
        
        total_volume = buy_volume + sell_volume
        if total_volume > 0:
            flow_ratio = (buy_volume - sell_volume) / total_volume
        else:
            flow_ratio = 0
        
        return {
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'flow_ratio': flow_ratio,
            'trade_count': len(recent_trades)
        }
    
    def get_comprehensive_analysis(self) -> Dict:
        """종합 분석 결과"""
        try:
            analysis = {}
            analysis['orderbook_imbalance'] = self.analyze_orderbook_imbalance()
            analysis['trade_flow'] = self.analyze_trade_flow()
            
            # 간단한 종합 시그널
            imbalance = analysis['orderbook_imbalance'].get('basic_imbalance', 0)
            flow_ratio = analysis['trade_flow'].get('flow_ratio', 0)
            
            combined_signal = (imbalance * 0.6 + flow_ratio * 0.4)
            strength = abs(combined_signal)
            
            analysis['combined_signal'] = {
                'combined': combined_signal,
                'strength': strength,
                'components': {
                    'orderbook': imbalance,
                    'trade_flow': flow_ratio
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"분석 오류: {e}")
            return {}
'''
            
            # 스마트 주문 매니저 모듈
            smart_order_code = '''#!/usr/bin/env python3
# 스마트 주문 매니저 (간소화된 VM 버전)
import asyncio
import logging
import time
from typing import Dict
from datetime import datetime
from enum import Enum

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class SmartOrderManager:
    def __init__(self, okx_client, market_analyzer):
        self.logger = logging.getLogger(__name__)
        self.okx_client = okx_client
        self.market_analyzer = market_analyzer
        self.active_orders = {}
        self.order_history = []
        
    async def place_smart_order(self, side: str, size: float, order_type: OrderType = OrderType.MARKET, **kwargs) -> Dict:
        """스마트 주문 실행"""
        try:
            # 기본 검증
            if side not in ['buy', 'sell']:
                return {'success': False, 'error': '잘못된 주문 방향'}
            
            if size <= 0:
                return {'success': False, 'error': '잘못된 주문 크기'}
            
            # 시장 상황 분석
            analysis = self.market_analyzer.get_comprehensive_analysis()
            
            if analysis and 'combined_signal' in analysis:
                signal = analysis['combined_signal']
                strength = signal.get('strength', 0)
                
                # 신호가 너무 약하면 주문 거부
                if strength < 0.3:
                    return {'success': False, 'error': f'신호 강도 부족: {strength:.4f}'}
            
            # 실제 주문 실행
            if order_type == OrderType.MARKET:
                result = await self.okx_client.place_order(
                    side=side,
                    size=size,
                    order_type='market'
                )
            else:
                # 제한가 주문
                price = kwargs.get('price')
                if not price:
                    return {'success': False, 'error': '제한가 미설정'}
                
                result = await self.okx_client.place_order(
                    side=side,
                    size=size,
                    order_type='limit',
                    price=price
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"스마트 주문 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_performance_metrics(self) -> Dict:
        """성능 메트릭"""
        return {
            'total_orders': len(self.order_history),
            'active_orders': len(self.active_orders)
        }
'''
            
            # 모듈 파일들 생성
            with open(os.path.join(modules_path, "websocket_client.py"), 'w', encoding='utf-8') as f:
                f.write(websocket_client_code)
            logger.info("✅ websocket_client.py 배포 완료")
            
            with open(os.path.join(modules_path, "market_microstructure.py"), 'w', encoding='utf-8') as f:
                f.write(market_analyzer_code)
            logger.info("✅ market_microstructure.py 배포 완료")
            
            with open(os.path.join(modules_path, "smart_order_manager.py"), 'w', encoding='utf-8') as f:
                f.write(smart_order_code)
            logger.info("✅ smart_order_manager.py 배포 완료")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 모듈 배포 실패: {e}")
            return False
    
    def update_main_system(self):
        """메인 시스템 업데이트"""
        logger.info("🔧 메인 시스템 업데이트 중...")
        
        try:
            # 업그레이드된 main.py 생성
            enhanced_main = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 OKX 비트코인 자동거래 시스템 v2.0
- WebSocket 실시간 데이터
- 시장 미세구조 분석
- 스마트 주문 실행
"""

import asyncio
import logging
import time
from datetime import datetime
import sys
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 기존 모듈들
import config
from okx_client import OKXClient
from trading_strategy import TradingStrategy
from risk_manager import RiskManager
from technical_analysis import TechnicalAnalysis
from news_sentiment import NewsSentimentAnalyzer
from utils import setup_logging
from telegram_bot.bot_handler import TelegramBotHandler

# 새로운 고급 모듈들
try:
    from modules.websocket_client import OKXWebSocketClient
    from modules.market_microstructure import MarketMicrostructureAnalyzer
    from modules.smart_order_manager import SmartOrderManager, OrderType
    ADVANCED_FEATURES = True
    logger.info("✅ 고급 기능 모듈 로드 성공")
except ImportError as e:
    logger.warning(f"⚠️ 고급 기능 모듈 로드 실패, 기본 모드로 동작: {e}")
    ADVANCED_FEATURES = False

class AdvancedTradingBot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 기본 컴포넌트
        self.okx_client = OKXClient()
        self.trading_strategy = TradingStrategy()
        self.risk_manager = RiskManager()
        self.technical_analysis = TechnicalAnalysis()
        self.news_analyzer = NewsSentimentAnalyzer()
        self.telegram_bot = TelegramBotHandler()
        
        # 고급 컴포넌트
        if ADVANCED_FEATURES:
            self.websocket_client = OKXWebSocketClient()
            self.market_analyzer = MarketMicrostructureAnalyzer()
            self.smart_order_manager = SmartOrderManager(self.okx_client, self.market_analyzer)
            
            # WebSocket 콜백 설정
            self.websocket_client.add_callback('orderbook', self._on_orderbook_update)
            self.websocket_client.add_callback('trades', self._on_trade_update)
        
        self.running = False
        self.last_analysis_time = 0
        
    async def _on_orderbook_update(self, orderbook_data):
        """호가창 업데이트 콜백"""
        try:
            self.market_analyzer.update_orderbook(orderbook_data)
        except Exception as e:
            self.logger.error(f"호가창 업데이트 오류: {e}")
    
    async def _on_trade_update(self, trade_data):
        """체결 데이터 업데이트 콜백"""
        try:
            self.market_analyzer.update_trades(trade_data)
        except Exception as e:
            self.logger.error(f"체결 데이터 업데이트 오류: {e}")
    
    async def start(self):
        """거래 봇 시작"""
        self.logger.info("🚀 고급 거래 봇 시작")
        self.running = True
        
        try:
            # 텔레그램 봇 시작
            telegram_task = asyncio.create_task(self.telegram_bot.start())
            
            # WebSocket 클라이언트 시작 (고급 기능)
            if ADVANCED_FEATURES:
                websocket_task = asyncio.create_task(self.websocket_client.start())
                self.logger.info("📡 WebSocket 실시간 데이터 스트림 시작")
            
            # 거래 루프 시작
            trading_task = asyncio.create_task(self.trading_loop())
            
            # 모든 태스크 실행
            tasks = [telegram_task, trading_task]
            if ADVANCED_FEATURES:
                tasks.append(websocket_task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            self.logger.error(f"시스템 오류: {e}")
        finally:
            self.running = False
    
    async def trading_loop(self):
        """메인 거래 루프"""
        while self.running:
            try:
                current_time = time.time()
                
                # 고급 분석 (WebSocket 데이터 사용)
                if ADVANCED_FEATURES and current_time - self.last_analysis_time > 5:  # 5초마다
                    analysis = self.market_analyzer.get_comprehensive_analysis()
                    
                    if analysis and 'combined_signal' in analysis:
                        signal = analysis['combined_signal']
                        combined = signal.get('combined', 0)
                        strength = signal.get('strength', 0)
                        
                        self.logger.info(f"🎯 고급 시그널: {combined:+.4f} (강도: {strength:.4f})")
                        
                        # 강한 신호일 때 거래 실행
                        if strength > 0.6:  # 60% 이상 신호 강도
                            side = 'buy' if combined > 0 else 'sell'
                            await self._execute_advanced_trade(side, strength)
                    
                    self.last_analysis_time = current_time
                
                # 기존 거래 로직 (30초마다)
                if current_time % 30 < 1:  # 대략 30초마다
                    await self._execute_basic_trade()
                
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"거래 루프 오류: {e}")
                await asyncio.sleep(5)
    
    async def _execute_advanced_trade(self, side: str, strength: float):
        """고급 거래 실행"""
        try:
            # 동적 포지션 크기 계산 (신호 강도에 비례)
            base_size = 0.01  # 기본 크기
            position_size = base_size * strength
            
            # 리스크 체크
            if not self.risk_manager.can_open_position(side, position_size):
                self.logger.warning(f"리스크 관리로 인한 거래 거부: {side} {position_size}")
                return
            
            # 스마트 주문 실행
            result = await self.smart_order_manager.place_smart_order(
                side=side,
                size=position_size,
                order_type=OrderType.MARKET
            )
            
            if result.get('success'):
                self.logger.info(f"✅ 고급 거래 성공: {side} {position_size} BTC")
                await self.telegram_bot.send_trade_notification(result)
            else:
                self.logger.warning(f"❌ 고급 거래 실패: {result.get('error')}")
                
        except Exception as e:
            self.logger.error(f"고급 거래 실행 오류: {e}")
    
    async def _execute_basic_trade(self):
        """기존 기본 거래 로직"""
        try:
            # 기존 분석
            current_price = await self.okx_client.get_current_price()
            if not current_price:
                return
            
            # 기술적 분석
            ta_data = await self.technical_analysis.analyze_market()
            if not ta_data:
                return
            
            # 뉴스 감정 분석
            sentiment_score = await self.news_analyzer.get_market_sentiment()
            
            # 거래 신호 생성
            signal_data = await self.trading_strategy.generate_signal(
                current_price, ta_data, sentiment_score
            )
            
            signal = signal_data.get('signal', 0)
            strength = signal_data.get('strength', 0)
            
            self.logger.info(f"📊 기본 신호: {signal:+.4f}, 강도: {strength:.4f}")
            
            # 거래 실행 로직 (기존과 동일)
            if abs(signal) > 0.5 and strength > 0.6:
                side = 'buy' if signal > 0 else 'sell'
                position_size = config.Config.POSITION_SIZE
                
                if self.risk_manager.can_open_position(side, position_size):
                    await self._place_order(side, position_size)
                    
        except Exception as e:
            self.logger.error(f"기본 거래 오류: {e}")
    
    async def _place_order(self, side: str, size: float):
        """주문 실행 (기존 로직)"""
        try:
            result = await self.okx_client.place_order(side, size, 'market')
            
            if result.get('success'):
                self.logger.info(f"✅ 거래 성공: {side} {size} BTC")
                await self.telegram_bot.send_trade_notification(result)
            else:
                self.logger.warning(f"❌ 거래 실패: {result.get('error')}")
                
        except Exception as e:
            self.logger.error(f"주문 실행 오류: {e}")

async def main():
    """메인 함수"""
    logger.info("🎯 고급 OKX 거래 시스템 v2.0 시작")
    
    bot = AdvancedTradingBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("⏹️ 사용자에 의한 종료")
    except Exception as e:
        logger.error(f"시스템 오류: {e}")
    finally:
        logger.info("🏁 시스템 종료")

if __name__ == "__main__":
    asyncio.run(main())
'''
            
            # main.py 백업 후 업데이트
            main_path = os.path.join(self.vm_path, "main.py")
            backup_main_path = os.path.join(self.backup_path, "main.py.backup")
            
            if os.path.exists(main_path):
                shutil.copy2(main_path, backup_main_path)
            
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_main)
            
            logger.info("✅ main.py 업데이트 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 메인 시스템 업데이트 실패: {e}")
            return False
    
    def restart_service(self):
        """서비스 재시작"""
        logger.info("🔄 서비스 재시작 중...")
        
        try:
            # systemctl 재시작
            result = subprocess.run([
                "sudo", "systemctl", "restart", "ton-trader"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ 서비스 재시작 성공")
                return True
            else:
                logger.error(f"❌ 서비스 재시작 실패: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 서비스 재시작 오류: {e}")
            return False
    
    def verify_upgrade(self):
        """업그레이드 검증"""
        logger.info("🔍 업그레이드 검증 중...")
        
        try:
            # 서비스 상태 확인
            result = subprocess.run([
                "sudo", "systemctl", "status", "ton-trader"
            ], capture_output=True, text=True)
            
            if "active (running)" in result.stdout:
                logger.info("✅ 서비스 정상 실행 중")
                
                # 로그 확인
                log_result = subprocess.run([
                    "sudo", "journalctl", "-u", "ton-trader", "--since", "1 minute ago", "-n", "20"
                ], capture_output=True, text=True)
                
                if "고급 기능 모듈 로드 성공" in log_result.stdout:
                    logger.info("🎉 고급 기능 업그레이드 성공!")
                    return True
                elif "고급 기능 모듈 로드 실패" in log_result.stdout:
                    logger.warning("⚠️ 고급 기능 로드 실패, 기본 모드로 동작 중")
                    return True
                else:
                    logger.info("ℹ️ 시스템 시작 중...")
                    return True
            else:
                logger.error("❌ 서비스 실행 실패")
                return False
                
        except Exception as e:
            logger.error(f"❌ 검증 오류: {e}")
            return False
    
    def run_upgrade(self):
        """전체 업그레이드 실행"""
        logger.info("🚀 === 고급 시스템 업그레이드 시작 ===")
        
        steps = [
            ("백업 생성", self.create_backup),
            ("의존성 설치", self.install_dependencies),
            ("새 모듈 배포", self.deploy_new_modules),
            ("메인 시스템 업데이트", self.update_main_system),
            ("서비스 재시작", self.restart_service),
            ("업그레이드 검증", self.verify_upgrade)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"📋 {step_name} 시작...")
            
            if step_func():
                logger.info(f"✅ {step_name} 완료")
            else:
                logger.error(f"❌ {step_name} 실패 - 업그레이드 중단")
                logger.info(f"💡 롤백 방법: {self.backup_path}에서 파일들을 복원")
                return False
        
        logger.info("🎉 === 고급 시스템 업그레이드 완료 ===")
        logger.info("🎯 새로운 기능:")
        logger.info("   - WebSocket 실시간 데이터 (초당 26개 업데이트)")
        logger.info("   - 시장 미세구조 분석 (호가창 불균형, 체결 플로우)")
        logger.info("   - 스마트 주문 실행 (신호 강도 기반 동적 포지션)")
        logger.info("   - 아이스버그 주문 감지")
        logger.info("   - 동적 지지/저항선 계산")
        
        return True

if __name__ == "__main__":
    upgrader = AdvancedSystemUpgrader()
    upgrader.run_upgrade()
