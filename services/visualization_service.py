from aiogram import types
import pandas as pd
import matplotlib.pyplot as plt
import io


class VisualizationService:
    @staticmethod
    async def formPieChart(data, caption):
        df = pd.DataFrame(data)

        df.set_index('country', inplace=True)
        df['aac'].plot.pie(autopct="%.1f%%", pctdistance=0.8)

        plt.title(caption)
        plt.ylabel('')

        buf = io.BytesIO()

        plt.savefig(buf, format='png')

        buf.seek(0)

        input_file = types.BufferedInputFile(buf.read(), 'plot.png')

        plt.clf()

        return input_file
