# import cv2
import numpy as np
from matplotlib import animation
from matplotlib.image import PcolorImage

# def get_q_snapshot(Q):
#	return Q_img

class GameAnimator:
    '''
        Usage:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        game = utils.GameAnimator(figure=fig, axes=ax, result=result_qplus)
        anim = game.animate(start_step = 0, stop_step = 5999)
        HTML(anim.to_html5_video())
    '''
    def __init__(self, figure, axes, result):

        self._figure = figure
        self._axes = axes
        self._result = result
        self._interval = 200
        self._total_frames = 1000

        # self._initialized = False
        # self.reset()

    def getTimeline(self, result, episode, start_step, stop_step):
        if episode is None:
            assert start_step is not None and stop_step is not None
            assert start_step < stop_step
            assert stop_step in result
            return start_step, stop_step
        else:
            start_step, stop_step = None, None
            assert episode <= result[next(reversed(result))]['episode']
            for step in range(len(result)):
                if episode == result[step]['episode']:
                    if start_step is None:
                        start_step = step
                    elif stop_step is None:
                        stop_step = step
                        assert start_step < stop_step
                        return start_step, stop_step

    def reset(self):
        self._axes_image = PcolorImage()
        self._axes.add_image(self._axes_image)
        self._initialized = True

    def renderFrame(self, step):
        # if not self._initialized:
        #     self.reset()
        frame = np.empty((6, 9))
        frame = self.drawValueFunction(self._result[step])
        # frame = self.drawGameEnv(frame, step_result)
        return (self._axes.pcolor(frame),)

    def drawValueFunction(self, step_result):
        return step_result['value_function'].max(1).reshape(6, 9)

    def animate(self, episode=None, start_step=None, stop_step=None):
        start_step, stop_step = self.getTimeline(self._result, episode,
                                                 start_step, stop_step)

        frame_step = float(stop_step - start_step) / self._total_frames
        frame_list = range(start_step, stop_step, int(frame_step))
        frame_iter = iter(frame_list)

        return animation.FuncAnimation(self._figure,
                                       self.renderFrame,
                                       frames=frame_iter,
                                       interval=self._interval,
                                       blit=True)
