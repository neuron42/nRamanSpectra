import ast

import numpy as np
from flask import request, render_template, redirect, Response
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.exceptions import HTTPException

from nRamanSpectra import app, db, admin
from nRamanSpectra.models import Spectra

basic_auth = BasicAuth(app)


class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise HTTPException('', Response('Password error.', 401,
                                             {'WWW-Authenticate': 'Basic'}))
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


# class MicroBlogModelView(sqla.ModelView):
#
#     def is_accessible(self):
#         return login.current_user.is_authenticated
#
#     def inaccessible_callback(self, name, **kwargs):
#         # redirect to login page if user doesn't have access
#         return redirect(url_for('login', next=request.url))


admin.add_view(ModelView(Spectra, db.session))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/spectras/create')
def create():
    return render_template('create.html')


@app.route('/spectras/classify')
def classify():
    return render_template('classify.html')


@app.route("/spectras")
def read_spectra():
    name = request.args.get("name")
    spectra = db.session.execute(db.select(Spectra).filter_by(name=name)).scalar_one()
    return render_template("spectra.html", name=spectra.name, data=spectra.data)


from utils.file_processor import FileProcessor

@app.post("/spectras")
def create_spectra():
    try:
        files = request.files.getlist("file")
        processed_data = [FileProcessor.parse_spectral_file(file) for file in files]
        
        spectra = Spectra(
            name=request.form["name"],
            data=processed_data
        )
        
        db.session.add(spectra)
        db.session.commit()
        return jsonify({
            "status": "success",
            "id": spectra.id,
            "name": spectra.name,
            "data_points": len(processed_data)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.post("/spectras/classify")
def classify_spectra():
    try:
        # 处理上传文件
        file = request.files["file"]
        sample_data = FileProcessor.parse_spectral_file(file)
        
        # 获取所有光谱数据的y值
        reference_spectras = Spectra.query.all()
        if not reference_spectras:
            abort(404, "No reference spectra found")
        
        # 提取样本数据y轴
        sample_y = np.array(sample_data)[:, 1].reshape(1, -1)
        
        # 批量计算相似度
        similarities = []
        for spectra in reference_spectras:
            reference_y = np.array(spectra.data)[:, 1].reshape(1, -1)
            similarity = cosine_similarity(sample_y, reference_y)[0][0]
            similarities.append((spectra.name, similarity))
        
        # 找出最佳匹配
        best_match = max(similarities, key=lambda x: x[1])
        
        return jsonify({
            "match": best_match[0],
            "similarity": float(best_match[1]),
            "evaluated_samples": len(similarities)
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
