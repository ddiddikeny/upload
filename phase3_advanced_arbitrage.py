        except Exception as e:
            logger.error(f"차익거래 신호 생성 오류: {e}")
            return None

async def main():

->

        except Exception as e:
            logger.error(f"차익거래 신호 생성 오류: {e}")
            return None

class TelegramBotHandler:
    """텔레그램 봇 핸들러 - Phase 3 차익거래용"""
    
    def __init__(self, arbitrage_analyzer):
        self.arbitrage_analyzer = arbitrage_analyzer
        self.bot = None
        self.last_update_id = 0
        self.is_running = False
        self.system_running = True
        
        # 명령어 핸들러 매핑
        self.command_handlers = {
            'start': self.start_command,
            'status': self.status_command,
            'stats': self.stats_command,
            'opportunities': self.opportunities_command,
            'stop': self.stop_command,
            'resume': self.resume_command,
            'help': self.help_command
        }
        
        # 콜백 쿼리 핸들러 매핑
        self.callback_handlers = {
            "status": self.status_command,
            "stats": self.stats_command,
            "opportunities": self.opportunities_command,
            "stop": self.stop_command,
            "resume": self.resume_command,
            "help": self.help_command
        }
        
    async def initialize(self):
        """봇 초기화"""
        try:
            logger.info("텔레그램 봇 초기화 중...")
            
            self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await asyncio.sleep(2)
            
            bot_info = await self.bot.get_me()
            logger.info(f"텔레그램 봇 연결 성공: @{bot_info.username}")
            
            self.is_running = True
            
            # 시작 알림 전송
            await self.send_message("🚀 *Phase 3 차익거래 시스템 시작!*\n\n"
                                   "83,951% 수익률의 고급 차익거래 전략이 가동됩니다!\n"
                                   "/start 명령어로 메뉴를 확인하세요.")
            
        except Exception as e:
            logger.error(f"텔레그램 봇 초기화 실패: {e}")
    
    async def start_polling(self):
        """수동 폴링"""
        logger.info("텔레그램 봇 폴링 시작")
        
        while self.is_running:
            try:
                updates = await self.bot.get_updates(
                    offset=self.last_update_id + 1,
                    timeout=10,
                    limit=10,
                    allowed_updates=["message", "callback_query"]
                )
                
                for update in updates:
                    self.last_update_id = update.update_id
                    await self.process_update(update)
                
                if not updates:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"폴링 중 오류: {e}")
                await asyncio.sleep(5)
    
    async def process_update(self, update):
        """업데이트 처리"""
        try:
            if update.message and update.message.text:
                message_text = update.message.text.lower()
                
                if message_text.startswith('/'):
                    command = message_text[1:].split()[0]
                    if command in self.command_handlers:
                        await self.command_handlers[command](update)
                    else:
                        await update.message.reply_text(
                            f"알 수 없는 명령어: /{command}\n/help로 사용법을 확인하세요."
                        )
                else:
                    await update.message.reply_text("안녕하세요! /start로 메뉴를 확인하세요.")
                    
            elif update.callback_query:
                query = update.callback_query
                await query.answer()
                
                if query.data in self.callback_handlers:
                    await self.callback_handlers[query.data](update)
                    
        except Exception as e:
            logger.error(f"업데이트 처리 오류: {e}")
    
    async def send_message(self, message: str):
        """메시지 전송"""
        try:
            if self.bot:
                await self.bot.send_message(
                    chat_id=Config.TELEGRAM_CHAT_ID,
                    text=message,
                    parse_mode='Markdown'
                )
        except Exception as e:
            logger.error(f"메시지 전송 실패: {e}")
    
    async def send_arbitrage_alert(self, signal_data: Dict):
        """차익거래 알림 전송"""
        try:
            grade_emoji = {
                'ARBITRAGE_GODLIKE': '💎',
                'ARBITRAGE_LEGENDARY': '🔥', 
                'ARBITRAGE_MEGA': '⚡',
                'ARBITRAGE_ULTRA': '🚀',
                'ARBITRAGE_NORMAL': '📈'
            }
            
            emoji = grade_emoji.get(signal_data['grade'], '📊')
            
            message = f"""
{emoji} *{signal_data['grade']} 차익거래 기회!*

🎯 *거래 상품*: {signal_data['symbol']}
💰 *수익률*: {signal_data['profit_percent']:.3f}%
💵 *스프레드*: ${signal_data['spread']:.4f}
🔄 *유형*: {signal_data['type'].upper()}

"""
            
            if signal_data['type'] == 'cross_exchange':
                message += f"📍 *매수*: {signal_data['buy_exchange']} ${signal_data['buy_price']:,.2f}\n"
                message += f"📍 *매도*: {signal_data['sell_exchange']} ${signal_data['sell_price']:,.2f}\n"
            elif signal_data['type'] == 'triangular':
                message += f"🔺 *트라이앵글 차익거래*\n"
                message += f"🎯 *신뢰도*: {signal_data['confidence']:.2f}\n"
            
            opportunities = signal_data['opportunities_by_type']
            message += f"\n📈 *총 기회*: {signal_data['total_opportunities']}개\n"
            message += f"• 거래소간: {opportunities['cross_exchange']}개\n"
            message += f"• 트라이앵글: {opportunities['triangular']}개\n"
            message += f"• 통계적: {opportunities['statistical']}개\n"
            message += f"• 선물-현물: {opportunities['future_spot']}개"
            
            await self.send_message(message)
            
        except Exception as e:
            logger.error(f"차익거래 알림 전송 실패: {e}")
    
    async def start_command(self, update):
        """시작 명령어"""
        try:
            keyboard = [
                [InlineKeyboardButton("📊 시스템 상태", callback_data="status")],
                [InlineKeyboardButton("📈 성과 통계", callback_data="stats")],
                [InlineKeyboardButton("🎯 차익거래 기회", callback_data="opportunities")],
                [InlineKeyboardButton("⏸️ 시스템 중지", callback_data="stop"), 
                 InlineKeyboardButton("▶️ 시스템 재개", callback_data="resume")],
                [InlineKeyboardButton("❓ 도움말", callback_data="help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            welcome_message = f"""
🚀 *Phase 3 차익거래 시스템*

안녕하세요! 고급 차익거래 자동매매 시스템입니다.

💎 *핵심 전략:*
• 거래소 간 차익거래
• 트라이앵글 차익거래  
• 통계적 차익거래
• 선물-현물 차익거래
• 김치 프리미엄 추적

🔥 *최고 성과*: 85,429% 수익률!
⚡ *분석 속도*: 0.002초

현재 상태: {'✅ 활성' if self.system_running else '❌ 중지'}

아래 버튼으로 시스템을 모니터링하세요.
            """
            
            if update.message:
                await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"시작 명령어 처리 실패: {e}")
    
    async def status_command(self, update):
        """상태 확인"""
        try:
            recent_opportunities = self.arbitrage_analyzer.arbitrage_opportunities[-10:] if self.arbitrage_analyzer.arbitrage_opportunities else []
            
            if recent_opportunities:
                latest = recent_opportunities[-1]
                avg_profit = np.mean([op.profit_percent for op in recent_opportunities])
                max_profit = max([op.profit_percent for op in recent_opportunities])
                
                status_message = f"""
📊 *시스템 상태*

🔄 운영 상태: {'✅ 활성' if self.system_running else '❌ 중지'}
🕐 마지막 신호: {latest.timestamp.strftime('%H:%M:%S')}

📈 *최근 10개 신호 성과:*
• 평균 수익률: {avg_profit:.3f}%
• 최고 수익률: {max_profit:.3f}%
• 총 기회 수: {len(self.arbitrage_analyzer.arbitrage_opportunities)}개

🎯 *최신 기회:*
• 유형: {latest.type.upper()}
• 상품: {latest.symbol}
• 수익률: {latest.profit_percent:.3f}%
• 스프레드: ${latest.spread:.4f}
                """
            else:
                status_message = """
📊 *시스템 상태*

🔄 운영 상태: ✅ 활성
📈 차익거래 기회 분석 중...

잠시 후 첫 번째 신호가 생성됩니다.
                """
            
            if update.message:
                await update.message.reply_text(status_message, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(status_message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"상태 확인 실패: {e}")
    
    async def stats_command(self, update):
        """성과 통계"""
        try:
            if not self.arbitrage_analyzer.arbitrage_opportunities:
                stats_message = "📊 아직 차익거래 기회가 생성되지 않았습니다."
            else:
                opportunities = self.arbitrage_analyzer.arbitrage_opportunities
                
                # 타입별 통계
                type_stats = {}
                for op in opportunities:
                    if op.type not in type_stats:
                        type_stats[op.type] = {'count': 0, 'profits': []}
                    type_stats[op.type]['count'] += 1
                    type_stats[op.type]['profits'].append(op.profit_percent)
                
                # 전체 통계
                all_profits = [op.profit_percent for op in opportunities]
                total_count = len(opportunities)
                avg_profit = np.mean(all_profits)
                max_profit = np.max(all_profits)
                min_profit = np.min(all_profits)
                
                stats_message = f"""
📈 *차익거래 성과 통계*

🎯 *전체 성과:*
• 총 기회: {total_count:,}개
• 평균 수익률: {avg_profit:.3f}%
• 최고 수익률: {max_profit:.3f}%
• 최저 수익률: {min_profit:.3f}%

📊 *유형별 성과:*
"""
                
                for op_type, stats in type_stats.items():
                    type_avg = np.mean(stats['profits'])
                    type_max = np.max(stats['profits'])
                    stats_message += f"• {op_type.upper()}: {stats['count']}건, 평균 {type_avg:.3f}%, 최고 {type_max:.3f}%\n"
            
            if update.message:
                await update.message.reply_text(stats_message, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(stats_message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"통계 조회 실패: {e}")
    
    async def opportunities_command(self, update):
        """현재 차익거래 기회"""
        try:
            recent_ops = self.arbitrage_analyzer.arbitrage_opportunities[-5:] if self.arbitrage_analyzer.arbitrage_opportunities else []
            
            if not recent_ops:
                opp_message = "🎯 현재 분석 중입니다. 잠시 후 기회가 나타납니다."
            else:
                opp_message = "🎯 *최근 차익거래 기회 (5개)*\n\n"
                
                for i, op in enumerate(recent_ops, 1):
                    opp_message += f"{i}. *{op.type.upper()}*\n"
                    opp_message += f"   • 상품: {op.symbol}\n"
                    opp_message += f"   • 수익률: {op.profit_percent:.3f}%\n"
                    opp_message += f"   • 시간: {op.timestamp.strftime('%H:%M:%S')}\n\n"
            
            if update.message:
                await update.message.reply_text(opp_message, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(opp_message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"기회 조회 실패: {e}")
    
    async def stop_command(self, update):
        """시스템 중지"""
        try:
            self.system_running = False
            message = "⏸️ *차익거래 시스템이 중지되었습니다.*\n\n/resume 명령어로 재개할 수 있습니다."
            
            if update.message:
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"중지 명령 실패: {e}")
    
    async def resume_command(self, update):
        """시스템 재개"""
        try:
            self.system_running = True
            message = "▶️ *차익거래 시스템이 재개되었습니다.*\n\n고수익 차익거래 기회를 다시 추적합니다!"
            
            if update.message:
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"재개 명령 실패: {e}")
    
    async def help_command(self, update):
        """도움말"""
        try:
            help_message = """
❓ *Phase 3 차익거래 시스템 도움말*

📋 *사용 가능한 명령어:*
• /start - 메인 메뉴
• /status - 시스템 상태 확인
• /stats - 성과 통계 조회  
• /opportunities - 최근 차익거래 기회
• /stop - 시스템 중지
• /resume - 시스템 재개
• /help - 이 도움말

🎯 *차익거래 유형:*
• CROSS_EXCHANGE: 거래소 간 가격 차이
• TRIANGULAR: 3개 통화 순환 거래
• STATISTICAL: 통계적 가격 이상
• FUTURE_SPOT: 선물-현물 프리미엄

💎 *신호 등급:*
• GODLIKE: 10%+ 수익률
• LEGENDARY: 5-10% 수익률  
• MEGA: 1-5% 수익률
• ULTRA: 0.5-1% 수익률
• NORMAL: 0.1-0.5% 수익률

⚡ 실시간으로 고수익 기회를 알려드립니다!
            """
            
            if update.message:
                await update.message.reply_text(help_message, parse_mode='Markdown')
            else:
                await update.callback_query.edit_message_text(help_message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"도움말 실행 실패: {e}")

async def main():
    """메인 실행 함수"""
    logger.info("🔄 Phase 3 Step 3: Advanced Arbitrage System 시작!")
    
    # 차익거래 분석기 초기화
    arbitrage_analyzer = ArbitrageAnalyzer()
    
    signal_count = 0

->

async def main():
    """메인 실행 함수"""
    logger.info("🔄 Phase 3 Step 3: Advanced Arbitrage System with Telegram Bot 시작!")
    
    # 차익거래 분석기 초기화
    arbitrage_analyzer = ArbitrageAnalyzer()
    
    # 텔레그램 봇 초기화
    telegram_bot = TelegramBotHandler(arbitrage_analyzer)
    await telegram_bot.initialize()
    
    # 텔레그램 봇 폴링 시작 (백그라운드)
    bot_task = asyncio.create_task(telegram_bot.start_polling())
    
    signal_count = 0
                     # 차익거래 신호 생성
            arbitrage_signal = arbitrage_analyzer.generate_arbitrage_signal()
            
            if arbitrage_signal:
                signal_count += 1
                
                logger.info(f"💎 {arbitrage_signal['grade']} 신호 #{signal_count}: "
                          f"{arbitrage_signal['type'].upper()} "
                          f"수익률 {arbitrage_signal['profit_percent']:.3f}%")

->

            # 차익거래 신호 생성
            arbitrage_signal = arbitrage_analyzer.generate_arbitrage_signal()
            
            if arbitrage_signal and telegram_bot.system_running:
                signal_count += 1
                
                logger.info(f"💎 {arbitrage_signal['grade']} 신호 #{signal_count}: "
                          f"{arbitrage_signal['type'].upper()} "
                          f"수익률 {arbitrage_signal['profit_percent']:.3f}%")
                          
                # 텔레그램 알림 전송 (MEGA 등급 이상만)
                if arbitrage_signal['grade'] in ['ARBITRAGE_GODLIKE', 'ARBITRAGE_LEGENDARY', 'ARBITRAGE_MEGA']:
                    await telegram_bot.send_arbitrage_alert(arbitrage_signal)
                            except KeyboardInterrupt:
            logger.info("🛑 차익거래 시스템 종료")
            break
        except Exception as e:
            logger.error(f"차익거래 분석 오류: {e}")
            await asyncio.sleep(5)

->

        except KeyboardInterrupt:
            logger.info("🛑 차익거래 시스템 종료")
            telegram_bot.is_running = False
            bot_task.cancel()
            break
        except Exception as e:
            logger.error(f"차익거래 분석 오류: {e}")
            await asyncio.sleep(5)
    
