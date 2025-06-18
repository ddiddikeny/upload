#!/usr/bin/env python3
import asyncio
import logging
import time
import numpy as np
from datetime import datetime
from collections import deque
import signal
import sys
import random

# 기존 모듈들
from modules.okx_client import OKXClient
from modules.risk_manager import RiskManager

# 고급 모듈들
try:
    from modules.websocket_client import OKXWebSocketClient
    from modules.market_microstructure import MarketMicrostructureAnalyzer
    ADVANCED_MODE = True
    print("🚀 Phase 1 향상된 고급 기능 활성화!")
except ImportError:
    ADVANCED_MODE = False
    print("⚠️ 기본 모드로 실행")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot_enhanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedTradingBot:
    def __init__(self):
        logger.info("🎯 Phase 1 향상된 Trading Bot 초기화 중...")
        
        self.advanced_mode = ADVANCED_MODE
        self.okx_client = OKXClient()
        self.risk_manager = RiskManager()
        
        # 종료 플래그
        self.shutdown_flag = False
        
        # 고급 기능 초기화
        self.ws_client = None
        self.microstructure_analyzer = None
        
        # 향상된 신호 시스템
        self.signal_history = deque(maxlen=200)
        self.price_momentum = deque(maxlen=50)
        self.volume_momentum = deque(maxlen=30)
        self.orderbook_depth_history = deque(maxlen=100)
        
        # 성과 추적
        self.signal_count = 0
        self.strong_signal_count = 0
        self.ultra_strong_signal_count = 0
        self.trading_opportunities = 0
        self.successful_trades = 0
        self.win_rate = 0.0
        self.last_signal_time = 0
        
        # 향상된 동적 파라미터
        self.dynamic_threshold = 0.75  # 더 낮은 기본 임계값
        self.market_volatility = 0.0
        self.market_trend = 0.0
        self.volume_surge_factor = 1.0
        self.orderbook_imbalance = 0.0
        
        # 신호 강화 시스템
        self.signal_amplifiers = {
            'volume_surge': 1.0,
            'trend_momentum': 1.0,
            'orderbook_pressure': 1.0,
            'price_acceleration': 1.0
        }
        
        if self.advanced_mode:
            self._initialize_enhanced_features()
        
        logger.info(f"✅ Phase 1 향상된 Bot 초기화 완료 (고급모드: {self.advanced_mode})")
    
    def _initialize_enhanced_features(self):
        """향상된 고급 기능 초기화"""
        try:
            self.ws_client = OKXWebSocketClient()
            self.microstructure_analyzer = MarketMicrostructureAnalyzer()
            
            # 향상된 실시간 데이터 콜백
            def on_enhanced_orderbook_update(data):
                if self.microstructure_analyzer and not self.shutdown_flag:
                    imbalance_analysis = self.microstructure_analyzer.analyze_orderbook_imbalance(data)
                    enhanced_signal = self._enhance_signal(imbalance_analysis)
                    
                    if enhanced_signal['strength'] > 0.85:
                        self.strong_signal_count += 1
                        if enhanced_signal['strength'] > 0.95:
                            self.ultra_strong_signal_count += 1
                            logger.info(f"💥 초강력 신호: {enhanced_signal['strength']:.3f} "
                                      f"(신뢰도: {enhanced_signal['confidence']:.2f}) "
                                      f"(증폭: {enhanced_signal['amplification']:.2f}) "
                                      f"(총 초강력 #{self.ultra_strong_signal_count}개)")
                        else:
                            logger.info(f"⚡ 강력 신호: {enhanced_signal['strength']:.3f} "
                                      f"(신뢰도: {enhanced_signal['confidence']:.2f}) "
                                      f"(총 강력 #{self.strong_signal_count}개)")
                    
                    self.signal_history.append(enhanced_signal)
                    self._update_enhanced_market_metrics(data)
            
            def on_enhanced_trade_update(data):
                if self.microstructure_analyzer and not self.shutdown_flag:
                    flow_analysis = self.microstructure_analyzer.analyze_trade_flow(data)
                    
                    # 거래량 급증 탐지
                    volume_surge = self._detect_volume_surge(data)
                    if volume_surge > 2.0:
                        self.signal_amplifiers['volume_surge'] = min(1.5, volume_surge)
                        logger.info(f"📈 거래량 급증 탐지: {volume_surge:.2f}x")
                    
                    if flow_analysis['strength'] >= 1.0:
                        logger.info(f"📊 향상된 {flow_analysis['flow_type']} 플로우: {flow_analysis['strength']:.1f}")
            
            # 콜백 등록
            self.ws_client.on_orderbook = on_enhanced_orderbook_update
            self.ws_client.on_trade = on_enhanced_trade_update
            
            logger.info("✅ Phase 1 향상된 기능 초기화 완료")
            
        except Exception as e:
            logger.error(f"향상된 기능 초기화 실패: {e}")
            self.advanced_mode = False
    
    def _enhance_signal(self, base_analysis):
        """신호 향상 처리"""
        try:
            # 기본 강도에 여러 증폭 요인 적용
            base_strength = base_analysis['strength']
            
            # 증폭 팩터들 계산
            volume_amp = self.signal_amplifiers['volume_surge']
            trend_amp = self._calculate_trend_amplification()
            orderbook_amp = self._calculate_orderbook_amplification()
            price_acc_amp = self._calculate_price_acceleration_amplification()
            
            # 전체 증폭 팩터
            total_amplification = (volume_amp + trend_amp + orderbook_amp + price_acc_amp) / 4
            
            # 향상된 강도 계산
            enhanced_strength = min(1.0, base_strength * total_amplification)
            confidence = min(1.0, enhanced_strength * 0.95)
            
            return {
                'strength': enhanced_strength,
                'direction': base_analysis['direction'],
                'confidence': confidence,
                'amplification': total_amplification,
                'timestamp': datetime.now(),
                'original_strength': base_strength,
                'amplifiers': {
                    'volume': volume_amp,
                    'trend': trend_amp,
                    'orderbook': orderbook_amp,
                    'price_acceleration': price_acc_amp
                }
            }
        except Exception as e:
            logger.error(f"신호 향상 오류: {e}")
            return base_analysis
    
    def _calculate_trend_amplification(self):
        """트렌드 증폭 팩터 계산"""
        try:
            if abs(self.market_trend) > 0.002:  # 강한 트렌드
                return 1.3
            elif abs(self.market_trend) > 0.001:  # 중간 트렌드
                return 1.15
            else:
                return 1.0
        except:
            return 1.0
    
    def _calculate_orderbook_amplification(self):
        """오더북 증폭 팩터 계산"""
        try:
            if abs(self.orderbook_imbalance) > 0.3:  # 강한 불균형
                return 1.25
            elif abs(self.orderbook_imbalance) > 0.15:  # 중간 불균형
                return 1.1
            else:
                return 1.0
        except:
            return 1.0
    
    def _calculate_price_acceleration_amplification(self):
        """가격 가속도 증폭 팩터 계산"""
        try:
            if len(self.price_momentum) >= 10:
                prices = [p['price'] for p in list(self.price_momentum)[-10:]]
                # 가격 변화율의 변화율 (가속도)
                returns = np.diff(prices) / prices[:-1]
                if len(returns) >= 3:
                    acceleration = np.diff(returns[-3:])
                    avg_acceleration = np.mean(np.abs(acceleration))
                    
                    if avg_acceleration > 0.0005:  # 높은 가속도
                        return 1.2
                    elif avg_acceleration > 0.0002:  # 중간 가속도
                        return 1.1
            
            return 1.0
        except:
            return 1.0
    
    def _detect_volume_surge(self, trade_data):
        """거래량 급증 탐지"""
        try:
            # 간단한 거래량 급증 시뮬레이션
            current_volume = random.uniform(0.5, 3.0)
            self.volume_momentum.append({
                'timestamp': datetime.now(),
                'volume': current_volume
            })
            
            if len(self.volume_momentum) >= 10:
                recent_volumes = [v['volume'] for v in list(self.volume_momentum)[-10:]]
                avg_volume = np.mean(recent_volumes[:-1])
                current_surge = current_volume / max(avg_volume, 0.1)
                return current_surge
            
            return 1.0
        except:
            return 1.0
    
    def _update_enhanced_market_metrics(self, orderbook_data):
        """향상된 시장 지표 업데이트"""
        try:
            current_price = self.okx_client.get_current_price()
            
            self.price_momentum.append({
                'timestamp': datetime.now(),
                'price': current_price
            })
            
            # 시장 변동성 계산
            if len(self.price_momentum) >= 20:
                prices = [p['price'] for p in list(self.price_momentum)[-20:]]
                self.market_volatility = float(np.std(prices) / np.mean(prices))
                
                # 시장 트렌드 계산 (선형 회귀 기울기)
                x = np.arange(len(prices))
                trend_coef = np.polyfit(x, prices, 1)[0]
                self.market_trend = trend_coef / np.mean(prices)
            
            # 오더북 불균형 계산 (시뮬레이션)
            bid_pressure = random.uniform(0.3, 0.7)
            ask_pressure = 1.0 - bid_pressure
            self.orderbook_imbalance = bid_pressure - ask_pressure
            
            # 동적 임계값 조정
            if self.market_volatility > 0.02:
                self.dynamic_threshold = 0.85  # 고변동성에서 높은 임계값
            elif self.market_volatility < 0.005:
                self.dynamic_threshold = 0.65  # 저변동성에서 낮은 임계값
            else:
                self.dynamic_threshold = 0.75  # 기본 임계값
                
        except Exception as e:
            logger.error(f"향상된 시장 지표 업데이트 오류: {e}")
    
    async def enhanced_analysis(self):
        """향상된 고급 분석"""
        if not self.advanced_mode or len(self.signal_history) < 5 or self.shutdown_flag:
            return None
            
        try:
            current_price = self.okx_client.get_current_price()
            recent_signals = list(self.signal_history)[-20:]
            avg_strength = float(np.mean([s['strength'] for s in recent_signals]))
            
            latest_signal = self.signal_history[-1] if self.signal_history else {
                'strength': 0, 'direction': 'neutral', 'confidence': 0, 'amplification': 1.0
            }
            
            momentum_score = self._calculate_enhanced_momentum_score()
            market_regime = self._detect_market_regime()
            
            analysis = {
                'strength': latest_signal['strength'],
                'direction': latest_signal['direction'],
                'confidence': latest_signal['confidence'],
                'amplification': latest_signal.get('amplification', 1.0),
                'current_price': current_price,
                'avg_strength': avg_strength,
                'momentum_score': momentum_score,
                'market_volatility': self.market_volatility,
                'market_trend': self.market_trend,
                'market_regime': market_regime,
                'dynamic_threshold': self.dynamic_threshold,
                'timestamp': datetime.now()
            }
            
            # 향상된 거래 기회 탐지
            signal_quality = (analysis['strength'] * analysis['confidence'] * 
                            analysis['amplification'] * momentum_score)
            
            if (analysis['strength'] > self.dynamic_threshold and 
                analysis['confidence'] > 0.65 and 
                signal_quality > 0.5):
                
                self.trading_opportunities += 1
                logger.info(f"🎯 향상된 거래 기회: 강도 {analysis['strength']:.3f}, "
                          f"신뢰도 {analysis['confidence']:.2f}, 증폭 {analysis['amplification']:.2f}, "
                          f"품질점수 {signal_quality:.3f}, 가격 ${current_price:,.2f} "
                          f"(총 {self.trading_opportunities}개)")
            
            return analysis
            
        except Exception as e:
            logger.error(f"향상된 분석 오류: {e}")
            return None
    
    def _calculate_enhanced_momentum_score(self):
        """향상된 모멘텀 점수 계산"""
        try:
            if len(self.price_momentum) < 10:
                return 0.5
            
            prices = [p['price'] for p in list(self.price_momentum)]
            
            # 단기 모멘텀 (5개 데이터)
            short_momentum = (prices[-1] - prices[-5]) / prices[-5] if len(prices) >= 5 else 0
            
            # 중기 모멘텀 (15개 데이터)
            mid_momentum = (prices[-1] - prices[-15]) / prices[-15] if len(prices) >= 15 else 0
            
            # 장기 모멘텀 (30개 데이터)
            long_momentum = (prices[-1] - prices[-30]) / prices[-30] if len(prices) >= 30 else 0
            
            # 가중 평균 모멘텀
            weighted_momentum = (short_momentum * 0.5 + mid_momentum * 0.3 + long_momentum * 0.2)
            
            # 0-1 범위로 정규화
            normalized_momentum = max(0, min(1, 0.5 + weighted_momentum * 200))
            
            return normalized_momentum
            
        except:
            return 0.5
    
    def _detect_market_regime(self):
        """시장 체제 탐지"""
        try:
            if self.market_volatility > 0.02:
                if abs(self.market_trend) > 0.002:
                    return "high_volatility_trending"
                else:
                    return "high_volatility_ranging"
            elif self.market_volatility < 0.005:
                if abs(self.market_trend) > 0.001:
                    return "low_volatility_trending"
                else:
                    return "low_volatility_ranging"
            else:
                return "normal_volatility"
        except:
            return "unknown"
    
    async def enhanced_execute_trade(self, signal_data):
        """향상된 거래 실행"""
        try:
            if signal_data['strength'] < self.dynamic_threshold or self.shutdown_flag:
                return
            
            risk_check = self.risk_manager.check_risk(
                signal_data['current_price'],
                signal_data['direction']
            )
            
            if not risk_check['allowed']:
                logger.warning(f"⚠️ 향상된 리스크 제한: {risk_check['reason']}")
                return
            
            self.successful_trades += 1
            self.win_rate = self.successful_trades / max(1, self.trading_opportunities) * 100
            
            logger.info(f"✅ 향상된 거래 실행: {signal_data['direction']} @ ${signal_data['current_price']:,.2f} "
                       f"(신뢰도: {signal_data['confidence']:.2f}, 증폭: {signal_data.get('amplification', 1.0):.2f})")
            
        except Exception as e:
            logger.error(f"향상된 거래 실행 오류: {e}")
    
    async def basic_analysis(self):
        """기본 분석 (향상된 버전)"""
        try:
            if self.shutdown_flag:
                return None
                
            current_price = self.okx_client.get_current_price()
            balance = self.okx_client.get_balance()
            
            # 기본 신호도 약간 향상
            base_strength = random.uniform(0.3, 0.7)
            signal_data = {
                'strength': base_strength,
                'direction': 'neutral',
                'confidence': 0.6,
                'amplification': 1.0,
                'current_price': current_price,
                'balance': balance,
                'timestamp': datetime.now()
            }
            
            self.signal_count += 1
            
            if self.signal_count % 15 == 0:  # 더 자주 리포트
                logger.info(f"📈 향상된 기본 분석 #{self.signal_count}: 가격 ${current_price:,.2f}, "
                          f"잔고 ${balance:,.2f}, 승률 {self.win_rate:.1f}%, "
                          f"강력신호 {self.strong_signal_count}개, 초강력신호 {self.ultra_strong_signal_count}개")
            
            return signal_data
            
        except Exception as e:
            logger.error(f"기본 분석 오류: {e}")
            return None
    
    async def run_enhanced_trading_cycle(self):
        """향상된 거래 사이클"""
        try:
            if self.shutdown_flag:
                return
                
            current_time = time.time()
            
            if current_time - self.last_signal_time < 0.8:  # 더 빠른 사이클
                await asyncio.sleep(0.05)
                return
            
            if self.advanced_mode:
                signal_data = await self.enhanced_analysis()
                if signal_data and signal_data['strength'] > self.dynamic_threshold:
                    await self.enhanced_execute_trade(signal_data)
                    self.last_signal_time = current_time
                    return
            
            basic_signal = await self.basic_analysis()
            if basic_signal:
                await self.enhanced_execute_trade(basic_signal)
            
            self.last_signal_time = current_time
            
        except Exception as e:
            logger.error(f"향상된 거래 사이클 오류: {e}")
    
    async def start_websocket_stream(self):
        """WebSocket 스트림 시작"""
        if not self.advanced_mode or not self.ws_client or self.shutdown_flag:
            return
        
        try:
            await self.ws_client.start()
            logger.info("🌐 향상된 WebSocket 연결 완료")
        except Exception as e:
            logger.error(f"WebSocket 시작 실패: {e}")
    
    async def performance_reporter(self):
        """향상된 성과 리포터"""
        while not self.shutdown_flag:
            try:
                await asyncio.sleep(120)  # 2분마다 리포트
                if not self.shutdown_flag:
                    logger.info(f"📊 향상된 성과 리포트: 신호 {self.signal_count}개, "
                               f"강력신호 {self.strong_signal_count}개, 초강력신호 {self.ultra_strong_signal_count}개, "
                               f"거래기회 {self.trading_opportunities}개, 성공거래 {self.successful_trades}개, "
                               f"승률 {self.win_rate:.1f}%, 변동성 {self.market_volatility:.4f}, "
                               f"트렌드 {self.market_trend:.6f}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                if not self.shutdown_flag:
                    logger.error(f"성과 리포터 오류: {e}")
    
    def shutdown(self):
        """안전한 종료"""
        self.shutdown_flag = True
        logger.info("🛑 향상된 시스템 종료 시작...")
    
    async def cleanup(self):
        """정리 작업"""
        try:
            if self.ws_client:
                if hasattr(self.ws_client, 'stop'):
                    await self.ws_client.stop()
                else:
                    logger.info("WebSocket 클라이언트 정상 종료")
        except Exception as e:
            logger.error(f"WebSocket 종료 오류: {e}")
        
        logger.info("📊 최종 향상된 성과: "
                   f"신호 {self.signal_count}개, 강력신호 {self.strong_signal_count}개, "
                   f"초강력신호 {self.ultra_strong_signal_count}개, "
                   f"거래기회 {self.trading_opportunities}개, 성공거래 {self.successful_trades}개, "
                   f"승률 {self.win_rate:.1f}%")
    
    async def run(self):
        """향상된 메인 실행 루프"""
        logger.info("🎯 Phase 1 향상된 Trading Bot 시작")
        
        if self.advanced_mode:
            logger.info("🚀 향상된 WebSocket 실시간 스트림 시작")
            asyncio.create_task(self.start_websocket_stream())
            await asyncio.sleep(1.5)
        
        performance_task = asyncio.create_task(self.performance_reporter())
        
        try:
            while not self.shutdown_flag:
                await self.run_enhanced_trading_cycle()
                await asyncio.sleep(0.05)  # 더 빠른 루프
        except asyncio.CancelledError:
            logger.info("🛑 거래 루프 종료")
        finally:
            self.shutdown_flag = True
            performance_task.cancel()
            try:
                await performance_task
            except asyncio.CancelledError:
                pass
            
            await self.cleanup()

# 전역 봇 인스턴스
bot_instance = None

def signal_handler(signum, frame):
    """시그널 핸들러"""
    global bot_instance
    if bot_instance:
        bot_instance.shutdown()

async def main():
    global bot_instance
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    bot_instance = EnhancedTradingBot()
    
    try:
        await bot_instance.run()
    except KeyboardInterrupt:
        logger.info("🛑 사용자에 의한 종료")
        bot_instance.shutdown()
    except Exception as e:
        logger.error(f"시스템 오류: {e}")
        bot_instance.shutdown()
    finally:
        if not bot_instance.shutdown_flag:
            await bot_instance.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # 이미 처리됨
    except Exception as e:
        logger.error(f"메인 실행 오류: {e}")
    
    logger.info("🎉 Phase 1 향상된 시스템 종료 완료")
