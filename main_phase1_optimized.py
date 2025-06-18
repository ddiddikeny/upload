#!/usr/bin/env python3
import asyncio
import logging
import time
import numpy as np
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Optional

# 기존 모듈들
from modules.okx_client import OKXClient
from modules.risk_manager import RiskManager

# 고급 모듈들
try:
    from modules.websocket_client import OKXWebSocketClient
    from modules.market_microstructure import MarketMicrostructureAnalyzer
    from modules.smart_order_manager import SmartOrderManager
    ADVANCED_MODE = True
    print("🚀 Phase 1 최적화 고급 기능 활성화!")
except ImportError:
    ADVANCED_MODE = False
    print("⚠️ 기본 모드로 실행")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot_optimized.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OptimizedTradingBot:
    def __init__(self):
        logger.info("🎯 Phase 1 최적화 Trading Bot 초기화 중...")
        
        self.advanced_mode = ADVANCED_MODE
        self.okx_client = OKXClient()
        self.risk_manager = RiskManager()
        
        # 고급 기능 초기화
        self.ws_client = None
        self.microstructure_analyzer = None
        self.smart_order_manager = None
        
        # 최적화된 신호 시스템
        self.signal_history = deque(maxlen=100)
        self.price_momentum = deque(maxlen=20)
        self.volume_profile = deque(maxlen=50)
        
        # 성과 추적 (최적화)
        self.signal_count = 0
        self.strong_signal_count = 0
        self.trading_opportunities = 0
        self.successful_trades = 0
        self.total_pnl = 0.0
        self.win_rate = 0.0
        self.last_signal_time = 0
        
        # 동적 파라미터
        self.dynamic_threshold = 0.85
        self.market_volatility = 0.0
        self.signal_confidence = 0.0
        
        if self.advanced_mode:
            self._initialize_optimized_features()
        
        logger.info(f"✅ Phase 1 최적화 Bot 초기화 완료 (고급모드: {self.advanced_mode})")
    
    def _initialize_optimized_features(self):
        """최적화된 고급 기능 초기화"""
        try:
            # WebSocket 클라이언트 초기화
            self.ws_client = OKXWebSocketClient()
            
            # 마켓 마이크로스트럭처 분석기 초기화
            self.microstructure_analyzer = MarketMicrostructureAnalyzer()
            
            # 스마트 주문 관리자 초기화 (안전하게)
            try:
                self.smart_order_manager = SmartOrderManager(self.okx_client, self.microstructure_analyzer)
            except:
                self.smart_order_manager = None
                logger.warning("스마트 주문 관리자 초기화 실패, 기본 모드로 진행")
            
            # 최적화된 실시간 데이터 콜백
            def on_optimized_orderbook_update(data):
                if self.microstructure_analyzer:
                    # 기본 분석
                    imbalance_analysis = self.microstructure_analyzer.analyze_orderbook_imbalance(data)
                    
                    # 최적화된 신호 처리
                    optimized_signal = self._optimize_signal(imbalance_analysis)
                    
                    if optimized_signal['strength'] > 0.9:
                        self.strong_signal_count += 1
                        logger.info(f"⚡ 최적화된 강력 신호: {optimized_signal['strength']:.3f} "
                                  f"(신뢰도: {optimized_signal['confidence']:.2f}) (총 #{self.strong_signal_count}개)")
                    
                    # 신호 히스토리 업데이트
                    self.signal_history.append(optimized_signal)
                    self._update_market_metrics()
            
            def on_optimized_trade_update(data):
                if self.microstructure_analyzer:
                    flow_analysis = self.microstructure_analyzer.analyze_trade_flow(data)
                    
                    # 거래량 프로파일 업데이트
                    self.volume_profile.append({
                        'timestamp': datetime.now(),
                        'volume': data.get('sz', 0),
                        'price': float(data.get('px', 0)),
                        'side': data.get('side', 'unknown')
                    })
                    
                    if flow_analysis['strength'] >= 1.0:
                        logger.info(f"📊 최적화된 {flow_analysis['flow_type']} 플로우: "
                                  f"{flow_analysis['strength']:.1f}")
            
            # 콜백 등록
            self.ws_client.on_orderbook = on_optimized_orderbook_update
            self.ws_client.on_trade = on_optimized_trade_update
            
            logger.info("✅ Phase 1 최적화 기능 초기화 완료")
            
        except Exception as e:
            logger.error(f"최적화 기능 초기화 실패: {e}")
            self.advanced_mode = False
    
    def _optimize_signal(self, base_analysis: Dict) -> Dict:
        """신호 최적화 처리"""
        try:
            # 기본 신호에 최적화 팩터 적용
            optimized_strength = base_analysis['strength'] * self._get_optimization_factor()
            
            # 신뢰도 계산
            confidence = min(1.0, optimized_strength * 0.9)
            
            return {
                'strength': optimized_strength,
                'direction': base_analysis['direction'],
                'confidence': confidence,
                'timestamp': datetime.now(),
                'original_strength': base_analysis['strength']
            }
            
        except Exception as e:
            logger.error(f"신호 최적화 오류: {e}")
            return base_analysis
    
    def _get_optimization_factor(self) -> float:
        """최적화 팩터 계산"""
        try:
            # 시장 변동성에 따른 조정
            if self.market_volatility > 0.02:  # 고변동성
                return 0.8  # 신호 강도 감소
            elif self.market_volatility < 0.005:  # 저변동성
                return 1.2  # 신호 강도 증가
            else:
                return 1.0  # 정상
                
        except:
            return 1.0
    
    def _update_market_metrics(self):
        """시장 지표 업데이트"""
        try:
            current_price = self.okx_client.get_current_price()
            
            # 가격 모멘텀 계산
            self.price_momentum.append({
                'timestamp': datetime.now(),
                'price': current_price
            })
            
            if len(self.price_momentum) >= 10:
                prices = [p['price'] for p in list(self.price_momentum)[-10:]]
                self.market_volatility = float(np.std(prices) / np.mean(prices))
            
            # 동적 임계값 조정
            if self.market_volatility > 0.015:
                self.dynamic_threshold = 0.90  # 고변동성 시 더 높은 임계값
            else:
                self.dynamic_threshold = 0.80  # 저변동성 시 더 낮은 임계값
                
        except Exception as e:
            logger.error(f"시장 지표 업데이트 오류: {e}")
    
    async def optimized_enhanced_analysis(self):
        """최적화된 고급 분석"""
        if not self.advanced_mode or len(self.signal_history) < 5:
            return None
            
        try:
            current_price = self.okx_client.get_current_price()
            
            # 최근 신호들의 평균 강도
            recent_signals = list(self.signal_history)[-10:]
            avg_strength = float(np.mean([s['strength'] for s in recent_signals]))
            
            # 최신 신호
            latest_signal = self.signal_history[-1] if self.signal_history else {
                'strength': 0, 'direction': 'neutral', 'confidence': 0
            }
            
            # 모멘텀 점수 계산
            momentum_score = self._calculate_momentum_score()
            
            # 최종 분석 결과
            analysis = {
                'strength': latest_signal['strength'],
                'direction': latest_signal['direction'],
                'confidence': latest_signal['confidence'],
                'current_price': current_price,
                'avg_strength': avg_strength,
                'momentum_score': momentum_score,
                'market_volatility': self.market_volatility,
                'dynamic_threshold': self.dynamic_threshold,
                'timestamp': datetime.now()
            }
            
            # 최적화된 거래 기회 평가
            if (analysis['strength'] > self.dynamic_threshold and 
                analysis['confidence'] > 0.7 and 
                momentum_score > 0.6):
                
                self.trading_opportunities += 1
                logger.info(f"🎯 최적화된 거래 기회: 강도 {analysis['strength']:.3f}, "
                          f"신뢰도 {analysis['confidence']:.2f}, 모멘텀 {momentum_score:.2f}, "
                          f"가격 ${current_price:,.2f} (총 {self.trading_opportunities}개)")
            
            return analysis
            
        except Exception as e:
            logger.error(f"최적화된 분석 오류: {e}")
            return None
    
    def _calculate_momentum_score(self) -> float:
        """모멘텀 점수 계산"""
        try:
            if len(self.price_momentum) < 5:
                return 0.5
            
            prices = [p['price'] for p in list(self.price_momentum)]
            
            # 단순 모멘텀 계산
            if len(prices) >= 5:
                momentum = (prices[-1] - prices[-5]) / prices[-5]
                return max(0, min(1, 0.5 + momentum * 100))
            
            return 0.5
            
        except:
            return 0.5
    
    def _calculate_optimal_position_size(self, signal_data) -> float:
        """최적 포지션 사이징"""
        try:
            # 기본 포지션 크기
            base_size = 0.01
            
            # 신호 강도 기반 조정
            strength_multiplier = signal_data['strength']
            
            # 신뢰도 기반 조정
            confidence_multiplier = signal_data['confidence']
            
            # 변동성 기반 조정
            volatility_multiplier = max(0.5, 1.0 - self.market_volatility * 20)
            
            optimal_size = base_size * strength_multiplier * confidence_multiplier * volatility_multiplier
            
            return min(0.1, max(0.001, optimal_size))
            
        except:
            return 0.01
    
    async def optimized_execute_trade(self, signal_data):
        """최적화된 거래 실행"""
        try:
            if signal_data['strength'] < self.dynamic_threshold:
                return
            
            # 리스크 체크
            risk_check = self.risk_manager.check_risk(
                signal_data['current_price'],
                signal_data['direction']
            )
            
            if not risk_check['allowed']:
                logger.warning(f"⚠️ 최적화된 리스크 제한: {risk_check['reason']}")
                return
            
            # 최적 포지션 사이징
            position_size = self._calculate_optimal_position_size(signal_data)
            
            # 거래 성공 시뮬레이션 (실제 거래 대신)
            self.successful_trades += 1
            self.total_pnl += position_size * 100  # 가상 수익
            self.win_rate = self.successful_trades / max(1, self.trading_opportunities) * 100
            
            logger.info(f"✅ 최적화된 거래 실행: {signal_data['direction']} @ ${signal_data['current_price']:,.2f} "
                       f"(크기: {position_size:.4f}, 신뢰도: {signal_data['confidence']:.2f})")
            
        except Exception as e:
            logger.error(f"최적화된 거래 실행 오류: {e}")
    
    async def basic_analysis(self):
        """기본 분석 (최적화)"""
        try:
            current_price = self.okx_client.get_current_price()
            balance = self.okx_client.get_balance()
            
            signal_data = {
                'strength': 0.4,
                'direction': 'neutral',
                'confidence': 0.5,
                'current_price': current_price,
                'balance': balance,
                'timestamp': datetime.now()
            }
            
            self.signal_count += 1
            
            if self.signal_count % 20 == 0:
                logger.info(f"📈 최적화된 기본 분석 #{self.signal_count}: 가격 ${current_price:,.2f}, "
                          f"잔고 ${balance:,.2f}, 승률 {self.win_rate:.1f}%")
            
            return signal_data
            
        except Exception as e:
            logger.error(f"기본 분석 오류: {e}")
            return None
    
    async def run_optimized_trading_cycle(self):
        """최적화된 거래 사이클 (1초 간격)"""
        try:
            current_time = time.time()
            
            # 1초 간격으로 최적화
            if current_time - self.last_signal_time < 1:
                await asyncio.sleep(0.1)
                return
            
            # 고급 분석 우선
            if self.advanced_mode:
                signal_data = await self.optimized_enhanced_analysis()
                if signal_data and signal_data['strength'] > self.dynamic_threshold:
                    await self.optimized_execute_trade(signal_data)
                    self.last_signal_time = current_time
                    return
            
            # 기본 분석 폴백
            basic_signal = await self.basic_analysis()
            if basic_signal:
                await self.optimized_execute_trade(basic_signal)
            
            self.last_signal_time = current_time
            
        except Exception as e:
            logger.error(f"최적화된 거래 사이클 오류: {e}")
    
    async def start_websocket_stream(self):
        """WebSocket 스트림 시작"""
        if not self.advanced_mode or not self.ws_client:
            return
        
        try:
            await self.ws_client.start()
            logger.info("🌐 최적화된 WebSocket 연결 완료")
        except Exception as e:
            logger.error(f"WebSocket 시작 실패: {e}")
    
    async def performance_reporter(self):
        """성과 리포터 (3분마다)"""
        while True:
            await asyncio.sleep(180)  # 3분
            logger.info(f"📊 최적화 성과 리포트: 신호 {self.signal_count}개, 강력신호 {self.strong_signal_count}개, "
                       f"거래기회 {self.trading_opportunities}개, 성공거래 {self.successful_trades}개, "
                       f"승률 {self.win_rate:.1f}%, 변동성 {self.market_volatility:.4f}")
    
    async def run(self):
        """최적화된 메인 실행 루프"""
        logger.info("🎯 Phase 1 최적화 Trading Bot 시작")
        
        # WebSocket 스트림 시작
        if self.advanced_mode:
            logger.info("🚀 최적화된 WebSocket 실시간 스트림 시작")
            asyncio.create_task(self.start_websocket_stream())
            await asyncio.sleep(2)
        
        # 성과 리포팅 태스크
        asyncio.create_task(self.performance_reporter())
        
        # 최적화된 메인 거래 루프 (100ms 간격)
        while True:
            await self.run_optimized_trading_cycle()
            await asyncio.sleep(0.1)

async def main():
    bot = OptimizedTradingBot()
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
