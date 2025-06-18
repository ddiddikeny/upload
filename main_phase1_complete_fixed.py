#!/usr/bin/env python3
import asyncio
import logging
import time
from datetime import datetime

# 기존 모듈들
from modules.okx_client import OKXClient
from modules.risk_manager import RiskManager

# 고급 모듈들
try:
    from modules.websocket_client import OKXWebSocketClient
    from modules.market_microstructure import MarketMicrostructureAnalyzer
    ADVANCED_MODE = True
    print("🚀 Phase 1 고급 기능 활성화!")
except ImportError:
    ADVANCED_MODE = False
    print("⚠️ 기본 모드로 실행")

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

class Phase1CompleteTradingBot:
    def __init__(self):
        logger.info("🎯 Phase 1 Complete Trading Bot 초기화 중...")
        
        self.advanced_mode = ADVANCED_MODE
        self.okx_client = OKXClient()
        self.risk_manager = RiskManager()
        
        # 고급 기능 초기화
        self.ws_client = None
        self.microstructure_analyzer = None
        self.latest_analysis = {'strength': 0, 'direction': 'neutral'}
        
        # 성과 추적
        self.signal_count = 0
        self.strong_signal_count = 0
        self.trading_opportunities = 0
        self.last_signal_time = 0
        
        if self.advanced_mode:
            self._initialize_advanced_features()
        
        logger.info(f"✅ Phase 1 Complete Bot 초기화 완료 (고급모드: {self.advanced_mode})")
    
    def _initialize_advanced_features(self):
        """고급 기능 초기화"""
        try:
            # WebSocket 클라이언트 초기화
            self.ws_client = OKXWebSocketClient()
            
            # 마켓 마이크로스트럭처 분석기 초기화
            self.microstructure_analyzer = MarketMicrostructureAnalyzer()
            
            # 실시간 데이터 콜백 설정
            def on_orderbook_update(data):
                if self.microstructure_analyzer:
                    analysis = self.microstructure_analyzer.analyze_orderbook_imbalance(data)
                    if analysis['strength'] > 0.9:
                        self.strong_signal_count += 1
                        logger.info(f"⚡ 매우 강한 오더북 신호: {analysis['strength']:.3f} (총 #{self.strong_signal_count}개)")
                    self.latest_analysis = analysis
            
            def on_trade_update(data):
                if self.microstructure_analyzer:
                    flow_analysis = self.microstructure_analyzer.analyze_trade_flow(data)
                    if flow_analysis['strength'] >= 1.0:
                        logger.info(f"📊 실시간 {flow_analysis['flow_type']} 플로우: {flow_analysis['strength']:.1f}")
            
            # 콜백 등록
            self.ws_client.on_orderbook = on_orderbook_update
            self.ws_client.on_trade = on_trade_update
            
            logger.info("✅ Phase 1 고급 기능 초기화 완료")
            
        except Exception as e:
            logger.error(f"고급 기능 초기화 실패: {e}")
            self.advanced_mode = False
    
    async def enhanced_analysis(self):
        """고급 분석 실행"""
        if not self.advanced_mode:
            return None
            
        try:
            # 현재 가격 (동기 호출 - await 제거됨)
            current_price = self.okx_client.get_current_price()
            
            # 실시간 분석 결과
            analysis = self.latest_analysis.copy()
            analysis['current_price'] = current_price
            analysis['timestamp'] = datetime.now()
            
            # 거래 기회 평가
            if analysis['strength'] > 0.85:
                self.trading_opportunities += 1
                logger.info(f"🎯 거래 기회 감지: 강도 {analysis['strength']:.3f}, 가격 ${current_price:,.2f} (총 {self.trading_opportunities}개)")
            
            return analysis
            
        except Exception as e:
            logger.error(f"고급 분석 오류: {e}")
            return None
    
    async def basic_analysis(self):
        """기본 분석 실행"""
        try:
            # 현재 가격 및 기본 데이터 (동기 호출 - await 제거됨)
            current_price = self.okx_client.get_current_price()
            balance = self.okx_client.get_balance()
            
            # 기본 신호 생성
            signal_data = {
                'strength': 0.3,
                'direction': 'neutral',
                'current_price': current_price,
                'balance': balance,
                'timestamp': datetime.now()
            }
            
            self.signal_count += 1
            
            if self.signal_count % 10 == 0:
                logger.info(f"📈 기본 분석 #{self.signal_count}: 가격 ${current_price:,.2f}, 잔고 ${balance:,.2f}")
            
            return signal_data
            
        except Exception as e:
            logger.error(f"기본 분석 오류: {e}")
            return None
    
    async def execute_trade(self, signal_data):
        """거래 실행"""
        try:
            if signal_data['strength'] < 0.6:
                return
            
            # 리스크 체크 (동기 호출)
            risk_check = self.risk_manager.check_risk(
                signal_data['current_price'],
                signal_data['direction']
            )
            
            if not risk_check['allowed']:
                logger.warning(f"⚠️ 리스크 제한: {risk_check['reason']}")
                return
            
            logger.info(f"✅ 거래 신호 실행 검토: {signal_data['direction']} @ ${signal_data['current_price']:,.2f}")
            
        except Exception as e:
            logger.error(f"거래 실행 오류: {e}")
    
    async def run_trading_cycle(self):
        """거래 사이클 실행"""
        try:
            current_time = time.time()
            
            # 신호 생성 간격 제어 (5초)
            if current_time - self.last_signal_time < 5:
                await asyncio.sleep(1)
                return
            
            # 고급 분석 우선 시도
            if self.advanced_mode:
                signal_data = await self.enhanced_analysis()
                if signal_data and signal_data['strength'] > 0.8:
                    await self.execute_trade(signal_data)
                    self.last_signal_time = current_time
                    return
            
            # 기본 분석으로 폴백
            basic_signal = await self.basic_analysis()
            if basic_signal:
                await self.execute_trade(basic_signal)
            
            self.last_signal_time = current_time
            
        except Exception as e:
            logger.error(f"거래 사이클 오류: {e}")
    
    async def start_websocket_stream(self):
        """WebSocket 스트림 시작"""
        if not self.advanced_mode or not self.ws_client:
            return
        
        try:
            await self.ws_client.start()
            logger.info("🌐 WebSocket 연결 완료")
        except Exception as e:
            logger.error(f"WebSocket 시작 실패: {e}")
    
    async def run(self):
        """메인 실행 루프"""
        logger.info("🎯 Phase 1 Complete Trading Bot 시작")
        
        # WebSocket 스트림 시작
        if self.advanced_mode:
            logger.info("🚀 WebSocket 실시간 스트림 시작")
            asyncio.create_task(self.start_websocket_stream())
            await asyncio.sleep(2)  # WebSocket 초기화 대기
        
        # 메인 거래 루프
        while True:
            await self.run_trading_cycle()
            await asyncio.sleep(1)

async def main():
    bot = Phase1CompleteTradingBot()
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 사용자에 의한 종료")
    except Exception as e:
        logger.error(f"시스템 오류: {e}")
    finally:
        if bot.ws_client:
            await bot.ws_client.close()

if __name__ == "__main__":
    asyncio.run(main())
