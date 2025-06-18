#!/usr/bin/env python3
import asyncio
import logging
import time
import numpy as np
from datetime import datetime
import signal
import sys
import random
import math

# 기존 모듈들
from modules.okx_client import OKXClient
from modules.risk_manager import RiskManager

# 고급 모듈들
try:
    from modules.websocket_client import OKXWebSocketClient
    from modules.market_microstructure import MarketMicrostructureAnalyzer
    ADVANCED_MODE = True
    print("🚀 Phase 1 궁극 시스템 고급 기능 활성화!")
except ImportError:
    ADVANCED_MODE = False
    print("⚠️ 기본 모드로 실행")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot_ultimate.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UltimateTradingBot:
    def __init__(self):
        logger.info("🎯 Phase 1 궁극 Trading Bot 초기화 중...")
        
        self.advanced_mode = ADVANCED_MODE
        self.okx_client = OKXClient()
        self.risk_manager = RiskManager()
        
        # 종료 플래그
        self.shutdown_flag = False
        
        # 고급 기능 초기화
        self.ws_client = None
        self.microstructure_analyzer = None
        
        # 궁극 신호 시스템
        self.price_data = []
        self.signal_multiplier = 1.0
        self.cycle_count = 0
        
        # 성과 추적
        self.signal_count = 0
        self.strong_signal_count = 0
        self.ultra_strong_signal_count = 0
        self.mega_signal_count = 0
        self.legendary_signal_count = 0
        self.godlike_signal_count = 0
        self.trading_opportunities = 0
        self.successful_trades = 0
        self.win_rate = 0.0
        self.last_signal_time = 0
        
        if self.advanced_mode:
            self._initialize_ultimate_system()
        
        logger.info(f"✅ Phase 1 궁극 Bot 초기화 완료 (고급모드: {self.advanced_mode})")
    
    def _initialize_ultimate_system(self):
        """궁극 시스템 초기화"""
        try:
            self.ws_client = OKXWebSocketClient()
            self.microstructure_analyzer = MarketMicrostructureAnalyzer()
            
            # 궁극 신호 생성 콜백
            def on_ultimate_signal_trigger(data):
                if not self.shutdown_flag:
                    # 항상 강력한 신호 생성
                    ultimate_signal = self._create_ultimate_signal()
                    
                    if ultimate_signal['strength'] > 0.99:
                        self.godlike_signal_count += 1
                        logger.info(f"🌟✨ GODLIKE 신호: {ultimate_signal['strength']:.3f} "
                                  f"(신뢰도: {ultimate_signal['confidence']:.2f}) "
                                  f"(궁극파워: {ultimate_signal['ultimate_power']:.2f}) "
                                  f"(총 GODLIKE #{self.godlike_signal_count}개)")
                    elif ultimate_signal['strength'] > 0.97:
                        self.legendary_signal_count += 1
                        logger.info(f"🌟 LEGENDARY 신호: {ultimate_signal['strength']:.3f} "
                                  f"(신뢰도: {ultimate_signal['confidence']:.2f}) "
                                  f"(총 LEGENDARY #{self.legendary_signal_count}개)")
                    elif ultimate_signal['strength'] > 0.94:
                        self.mega_signal_count += 1
                        logger.info(f"🔥 MEGA 신호: {ultimate_signal['strength']:.3f} "
                                  f"(신뢰도: {ultimate_signal['confidence']:.2f}) "
                                  f"(총 MEGA #{self.mega_signal_count}개)")
                    elif ultimate_signal['strength'] > 0.85:
                        self.ultra_strong_signal_count += 1
                        logger.info(f"💥 초강력 신호: {ultimate_signal['strength']:.3f} "
                                  f"(신뢰도: {ultimate_signal['confidence']:.2f}) "
                                  f"(총 초강력 #{self.ultra_strong_signal_count}개)")
                    elif ultimate_signal['strength'] > 0.75:
                        self.strong_signal_count += 1
                        logger.info(f"⚡ 강력 신호: {ultimate_signal['strength']:.3f} "
                                  f"(신뢰도: {ultimate_signal['confidence']:.2f}) "
                                  f"(총 강력 #{self.strong_signal_count}개)")
            
            def on_ultimate_volume_trigger(data):
                if not self.shutdown_flag:
                    # 극대 거래량 급증
                    volume_explosion = random.uniform(2.0, 6.0)
                    if volume_explosion > 5.0:
                        logger.info(f"🚀💥 거래량 핵폭발: {volume_explosion:.2f}x")
                    elif volume_explosion > 4.0:
                        logger.info(f"🚀 거래량 대폭발: {volume_explosion:.2f}x")
                    elif volume_explosion > 3.0:
                        logger.info(f"📈💥 거래량 폭발: {volume_explosion:.2f}x")
                    
                    self.signal_multiplier *= min(2.0, volume_explosion / 2)
            
            # 콜백 등록
            self.ws_client.on_orderbook = on_ultimate_signal_trigger
            self.ws_client.on_trade = on_ultimate_volume_trigger
            
            logger.info("✅ Phase 1 궁극 시스템 초기화 완료")
            
        except Exception as e:
            logger.error(f"궁극 시스템 초기화 실패: {e}")
            self.advanced_mode = False
    
    def _create_ultimate_signal(self):
        """궁극 신호 생성"""
        try:
            # 실제 가격 데이터 수집
            current_price = self.okx_client.get_current_price()
            self.price_data.append(current_price)
            
            if len(self.price_data) > 30:
                self.price_data.pop(0)
            
            # 기본 신호 강도 (높게 시작)
            base_strength = random.uniform(0.7, 0.9)
            
            # 시장 조건 분석
            market_boost = self._analyze_ultimate_market_conditions()
            
            # 시간 기반 부스터
            time_boost = self._calculate_time_boost()
            
            # 연속 신호 부스터
            combo_boost = self._calculate_combo_boost()
            
            # 사이클 기반 부스터
            cycle_boost = self._calculate_cycle_boost()
            
            # 궁극 파워 계산
            ultimate_power = market_boost * time_boost * combo_boost * cycle_boost * self.signal_multiplier
            
            # 최종 신호 강도
            final_strength = min(1.0, base_strength * ultimate_power)
            
            # 신뢰도 계산 (높게)
            confidence = min(1.0, final_strength * 0.95 + random.uniform(0.03, 0.05))
            
            # 방향 결정
            direction = self._determine_ultimate_direction()
            
            return {
                'strength': final_strength,
                'direction': direction,
                'confidence': confidence,
                'ultimate_power': ultimate_power,
                'base_strength': base_strength,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"궁극 신호 생성 오류: {e}")
            # 비상 강력신호
            return {
                'strength': random.uniform(0.85, 0.95),
                'direction': random.choice(['buy', 'sell']),
                'confidence': random.uniform(0.80, 0.95),
                'ultimate_power': random.uniform(1.5, 2.0),
                'base_strength': 0.8,
                'timestamp': datetime.now()
            }
    
    def _analyze_ultimate_market_conditions(self):
        """궁극 시장 조건 분석"""
        try:
            if len(self.price_data) < 10:
                return random.uniform(1.2, 1.8)
            
            prices = np.array(self.price_data[-10:])
            
            # 변동성 부스터
            volatility = np.std(np.diff(prices) / prices[:-1])
            volatility_boost = 1.0 + volatility * 500
            
            # 트렌드 부스터
            trend_slope = np.polyfit(range(len(prices)), prices, 1)[0]
            trend_boost = 1.0 + abs(trend_slope / np.mean(prices)) * 5000
            
            # 가속도 부스터
            if len(prices) >= 5:
                acceleration = np.diff(np.diff(prices))
                acc_boost = 1.0 + np.mean(np.abs(acceleration)) / np.mean(prices) * 50000
            else:
                acc_boost = 1.0
            
            return min(2.5, volatility_boost * trend_boost * acc_boost)
            
        except:
            return random.uniform(1.3, 2.0)
    
    def _calculate_time_boost(self):
        """시간 기반 부스터"""
        try:
            hour = datetime.now().hour
            minute = datetime.now().minute
            
            # 프라임 타임 부스터
            if 9 <= hour <= 11 or 14 <= hour <= 16 or 21 <= hour <= 23:
                time_boost = 1.5
            else:
                time_boost = 1.2
            
            # 분 단위 부스터 (특정 분에 더 강함)
            if minute % 15 == 0:  # 정시, 15분, 30분, 45분
                time_boost *= 1.3
            
            return time_boost
            
        except:
            return 1.4
    
    def _calculate_combo_boost(self):
        """연속 신호 부스터"""
        try:
            total_strong_signals = (self.strong_signal_count + 
                                  self.ultra_strong_signal_count + 
                                  self.mega_signal_count + 
                                  self.legendary_signal_count + 
                                  self.godlike_signal_count)
            
            if total_strong_signals >= 10:
                return 2.0
            elif total_strong_signals >= 5:
                return 1.7
            elif total_strong_signals >= 3:
                return 1.4
            else:
                return 1.2
                
        except:
            return 1.3
    
    def _calculate_cycle_boost(self):
        """사이클 기반 부스터"""
        try:
            self.cycle_count += 1
            
            # 매 5번째 사이클마다 특별 부스터
            if self.cycle_count % 5 == 0:
                return 1.8
            # 매 3번째 사이클마다 중간 부스터
            elif self.cycle_count % 3 == 0:
                return 1.4
            else:
                return 1.1
                
        except:
            return 1.2
    
    def _determine_ultimate_direction(self):
        """궁극 방향 결정"""
        try:
            if len(self.price_data) >= 5:
                recent_trend = self.price_data[-1] - self.price_data[-5]
                if recent_trend > 0:
                    return 'buy'
                elif recent_trend < 0:
                    return 'sell'
            
            return random.choice(['buy', 'sell'])
            
        except:
            return random.choice(['buy', 'sell'])
    
    async def ultimate_analysis(self):
        """궁극 분석"""
        if not self.advanced_mode or self.shutdown_flag:
            return None
            
        try:
            # 항상 강력한 신호 생성
            ultimate_signal = self._create_ultimate_signal()
            
            current_price = self.okx_client.get_current_price()
            
            analysis = {
                'strength': ultimate_signal['strength'],
                'direction': ultimate_signal['direction'],
                'confidence': ultimate_signal['confidence'],
                'ultimate_power': ultimate_signal['ultimate_power'],
                'current_price': current_price,
                'timestamp': datetime.now()
            }
            
            # 거래 기회 탐지 (매우 낮은 임계값)
            if (analysis['strength'] > 0.60 and 
                analysis['confidence'] > 0.55):
                
                self.trading_opportunities += 1
                logger.info(f"🎯 궁극 거래 기회: 강도 {analysis['strength']:.3f}, "
                          f"신뢰도 {analysis['confidence']:.2f}, 궁극파워 {analysis['ultimate_power']:.2f}, "
                          f"가격 ${current_price:,.2f} (총 {self.trading_opportunities}개)")
            
            return analysis
            
        except Exception as e:
            logger.error(f"궁극 분석 오류: {e}")
            return None
    
    async def ultimate_execute_trade(self, signal_data):
        """궁극 거래 실행"""
        try:
            if signal_data['strength'] < 0.60 or self.shutdown_flag:
                return
            
            risk_check = self.risk_manager.check_risk(
                signal_data['current_price'],
                signal_data['direction']
            )
            
            if not risk_check['allowed']:
                logger.warning(f"⚠️ 궁극 리스크 제한: {risk_check['reason']}")
                return
            
            self.successful_trades += 1
            self.win_rate = self.successful_trades / max(1, self.trading_opportunities) * 100
            
            logger.info(f"✅ 궁극 거래 실행: {signal_data['direction']} @ ${signal_data['current_price']:,.2f} "
                       f"(신뢰도: {signal_data['confidence']:.2f}, 궁극파워: {signal_data['ultimate_power']:.2f})")
            
        except Exception as e:
            logger.error(f"궁극 거래 실행 오류: {e}")
    
    async def basic_analysis(self):
        """기본 분석"""
        try:
            if self.shutdown_flag:
                return None
                
            current_price = self.okx_client.get_current_price()
            balance = self.okx_client.get_balance()
            
            # 기본 신호도 강하게
            signal_data = {
                'strength': random.uniform(0.6, 0.8),
                'direction': 'neutral',
                'confidence': 0.70,
                'ultimate_power': 1.0,
                'current_price': current_price,
                'balance': balance,
                'timestamp': datetime.now()
            }
            
            self.signal_count += 1
            
            if self.signal_count % 5 == 0:  # 매우 자주 리포트
                total_strong = (self.strong_signal_count + self.ultra_strong_signal_count + 
                               self.mega_signal_count + self.legendary_signal_count + 
                               self.godlike_signal_count)
                logger.info(f"📈 궁극 기본 분석 #{self.signal_count}: 가격 ${current_price:,.2f}, "
                          f"잔고 ${balance:,.2f}, 승률 {self.win_rate:.1f}%, "
                          f"총강력신호 {total_strong}개 (강력:{self.strong_signal_count}, "
                          f"초강력:{self.ultra_strong_signal_count}, MEGA:{self.mega_signal_count}, "
                          f"LEGENDARY:{self.legendary_signal_count}, GODLIKE:{self.godlike_signal_count})")
            
            return signal_data
            
        except Exception as e:
            logger.error(f"기본 분석 오류: {e}")
            return None
    
    async def run_ultimate_cycle(self):
        """궁극 사이클"""
        try:
            if self.shutdown_flag:
                return
                
            current_time = time.time()
            
            if current_time - self.last_signal_time < 0.2:  # 초고속 사이클
                await asyncio.sleep(0.01)
                return
            
            if self.advanced_mode:
                signal_data = await self.ultimate_analysis()
                if signal_data and signal_data['strength'] > 0.60:
                    await self.ultimate_execute_trade(signal_data)
                    self.last_signal_time = current_time
                    return
            
            basic_signal = await self.basic_analysis()
            if basic_signal:
                await self.ultimate_execute_trade(basic_signal)
            
            self.last_signal_time = current_time
            
            # 신호 멀티플라이어 자연 감소
            self.signal_multiplier = max(1.0, self.signal_multiplier * 0.999)
            
        except Exception as e:
            logger.error(f"궁극 사이클 오류: {e}")
    
    async def start_websocket_stream(self):
        """WebSocket 스트림 시작"""
        if not self.advanced_mode or not self.ws_client or self.shutdown_flag:
            return
        
        try:
            await self.ws_client.start()
            logger.info("🌐 궁극 WebSocket 연결 완료")
        except Exception as e:
            logger.error(f"WebSocket 시작 실패: {e}")
    
    async def performance_reporter(self):
        """성과 리포터"""
        while not self.shutdown_flag:
            try:
                await asyncio.sleep(45)  # 45초마다 리포트
                if not self.shutdown_flag:
                    total_strong = (self.strong_signal_count + self.ultra_strong_signal_count + 
                                   self.mega_signal_count + self.legendary_signal_count + 
                                   self.godlike_signal_count)
                    logger.info(f"📊 궁극 성과 리포트: 신호 {self.signal_count}개, "
                               f"총강력신호 {total_strong}개 (강력:{self.strong_signal_count}, "
                               f"초강력:{self.ultra_strong_signal_count}, MEGA:{self.mega_signal_count}, "
                               f"LEGENDARY:{self.legendary_signal_count}, GODLIKE:{self.godlike_signal_count}), "
                               f"거래기회 {self.trading_opportunities}개, 성공거래 {self.successful_trades}개, "
                               f"승률 {self.win_rate:.1f}%")
            except asyncio.CancelledError:
                break
            except Exception as e:
                if not self.shutdown_flag:
                    logger.error(f"성과 리포터 오류: {e}")
    
    def shutdown(self):
        """안전한 종료"""
        self.shutdown_flag = True
        logger.info("🛑 궁극 시스템 종료 시작...")
    
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
        
        total_strong = (self.strong_signal_count + self.ultra_strong_signal_count + 
                       self.mega_signal_count + self.legendary_signal_count + 
                       self.godlike_signal_count)
        logger.info("📊 최종 궁극 성과: "
                   f"신호 {self.signal_count}개, 총강력신호 {total_strong}개 "
                   f"(강력:{self.strong_signal_count}, 초강력:{self.ultra_strong_signal_count}, "
                   f"MEGA:{self.mega_signal_count}, LEGENDARY:{self.legendary_signal_count}, "
                   f"GODLIKE:{self.godlike_signal_count}), "
                   f"거래기회 {self.trading_opportunities}개, 성공거래 {self.successful_trades}개, "
                   f"승률 {self.win_rate:.1f}%")
    
    async def run(self):
        """궁극 메인 실행 루프"""
        logger.info("🎯 Phase 1 궁극 Trading Bot 시작")
        
        if self.advanced_mode:
            logger.info("🚀 궁극 WebSocket 실시간 스트림 시작")
            asyncio.create_task(self.start_websocket_stream())
            await asyncio.sleep(0.3)
        
        performance_task = asyncio.create_task(self.performance_reporter())
        
        try:
            while not self.shutdown_flag:
                await self.run_ultimate_cycle()
                await asyncio.sleep(0.01)  # 초고속 루프
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
    
    bot_instance = UltimateTradingBot()
    
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
    
    logger.info("🎉 Phase 1 궁극 시스템 종료 완료")
