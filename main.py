"""Duckshot entry point. Works on desktop (python main.py) and in the browser (pygbag)."""
import asyncio

import pygame

from config import settings
from session_manager import SessionManager


async def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    manager = SessionManager(screen)

    while manager.running:
        clock.tick(settings.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.quit()
            else:
                manager.handle_event(event)

        manager.update()
        manager.draw()
        pygame.display.flip()

        await asyncio.sleep(0)  # yield to the browser (required by Pygbag)

    pygame.quit()


asyncio.run(main())